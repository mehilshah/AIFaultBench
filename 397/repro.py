#!/usr/bin/env python3
"""Deterministic ViT repro harness for bug 397.

This script runs the same tiny ViT training job twice with the same seed and
once with a different seed. If the implementation is deterministic under the
reported seed/reset pattern, the two same-seed runs should match exactly.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from timm.models.vision_transformer import VisionTransformer  # noqa: E402


def set_seed(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.enabled = False


def build_dataset(seed: int) -> TensorDataset:
    """Create a tiny deterministic binary classification dataset."""
    grid = torch.linspace(-1.0, 1.0, 32)
    yy, xx = torch.meshgrid(grid, grid, indexing="ij")
    base0 = torch.stack([xx, yy, xx + yy], dim=0)
    base1 = torch.stack([1.0 - xx, 1.0 - yy, xx - yy], dim=0)

    images = []
    labels = []
    for idx in range(16):
        label = idx % 2
        labels.append(label)
        pattern = base0 if label == 0 else base1
        # Deterministic sample-specific offset keeps the dataset non-trivial.
        offset = (idx + 1) * 0.01
        images.append(pattern + offset)

    images = torch.stack(images, dim=0).to(torch.float32)
    labels = torch.tensor(labels, dtype=torch.long)

    # Shuffle with a local generator to keep the dataset order stable for a seed.
    generator = torch.Generator()
    generator.manual_seed(seed)
    order = torch.randperm(len(labels), generator=generator)
    return TensorDataset(images[order], labels[order])


def hash_state(model: nn.Module) -> str:
    hasher = hashlib.sha256()
    for name, tensor in model.state_dict().items():
        hasher.update(name.encode("utf-8"))
        hasher.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return hasher.hexdigest()


def run_once(seed: int) -> dict[str, object]:
    set_seed(seed)
    dataset = build_dataset(seed)
    loader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=0)

    model = VisionTransformer(
        img_size=32,
        patch_size=4,
        in_chans=3,
        num_classes=2,
        embed_dim=32,
        depth=2,
        num_heads=4,
        mlp_ratio=2.0,
        drop_rate=0.1,
        pos_drop_rate=0.1,
        attn_drop_rate=0.1,
        drop_path_rate=0.1,
        weight_init="",
    )
    model.train()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    epoch_losses: list[float] = []

    for _ in range(2):
        epoch_loss = 0.0
        for batch_images, batch_labels in loader:
            optimizer.zero_grad(set_to_none=True)
            logits = model(batch_images)
            loss = criterion(logits, batch_labels)
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item())
        epoch_losses.append(epoch_loss)

    model.eval()
    with torch.no_grad():
        logits = model(dataset.tensors[0])
        predictions = logits.argmax(dim=1).tolist()

    return {
        "seed": seed,
        "losses": epoch_losses,
        "predictions": predictions,
        "state_hash": hash_state(model),
    }


def main() -> int:
    runs = [run_once(42), run_once(42), run_once(43)]
    same_seed_equal = runs[0] == runs[1]
    different_seed_equal = runs[0] == runs[2]

    summary = {
        "same_seed_equal": same_seed_equal,
        "different_seed_equal": different_seed_equal,
        "runs": runs,
    }

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
