#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import torch
except Exception as exc:  # pragma: no cover - import-time environment check
    print(f"TORCH_IMPORT_ERROR: {exc}", file=sys.stderr)
    raise


REPO_ROOT = Path(__file__).resolve().parent
CODEBASE_ROOT = REPO_ROOT / "codebase"
if str(CODEBASE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODEBASE_ROOT))

import timm  # noqa: E402


@dataclass
class RunResult:
    mode: str
    losses: list[float]
    elapsed_s: float
    bad_step: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=int(os.environ.get("STEPS", "16")))
    parser.add_argument("--warmup-steps", type=int, default=int(os.environ.get("WARMUP_STEPS", "8")))
    parser.add_argument("--batch-size", type=int, default=int(os.environ.get("BATCH_SIZE", "1")))
    parser.add_argument("--image-size", type=int, default=int(os.environ.get("IMAGE_SIZE", "224")))
    parser.add_argument(
        "--pretrained",
        action=argparse.BooleanOptionalAction,
        default=os.environ.get("PRETRAINED", "1") != "0",
    )
    parser.add_argument(
        "--mode",
        choices=("eager", "compiled", "both"),
        default=os.environ.get("MODE", "both"),
    )
    return parser.parse_args()


def seed_everything(seed: int = 0) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def make_batch(batch_size: int, image_size: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    inputs = torch.randn(batch_size, 3, image_size, image_size, device=device, dtype=torch.float32)
    labels = torch.randint(0, 2, (batch_size, 1), device=device, dtype=torch.float32)
    return inputs, labels


def build_model(pretrained: bool, device: torch.device, compiled: bool) -> torch.nn.Module:
    model = timm.create_model(
        "tiny_vit_21m_224.dist_in22k_ft_in1k",
        pretrained=pretrained,
        num_classes=1,
    ).to(device)
    if compiled:
        model = torch.compile(model, fullgraph=True, backend="inductor")
    return model


def train_one(model: torch.nn.Module, *, batch_size: int, image_size: int, steps: int, warmup_steps: int, device: torch.device, mode: str) -> RunResult:
    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)

    model.train()
    for _ in range(warmup_steps):
        inputs, _ = make_batch(batch_size, image_size, device)
        with torch.no_grad(), torch.amp.autocast(device_type="cuda", dtype=torch.bfloat16):
            _ = model(inputs)

    losses: list[float] = []
    bad_step: int | None = None
    start = time.perf_counter()
    for step in range(steps):
        inputs, labels = make_batch(batch_size, image_size, device)
        optimizer.zero_grad(set_to_none=True)
        with torch.amp.autocast(device_type="cuda", dtype=torch.bfloat16):
            preds = model(inputs)
            loss = criterion(preds, labels)
        if not torch.isfinite(loss):
            bad_step = step
            losses.append(float("nan"))
            break
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().float().item()))
        if step == 0 or (step + 1) % 4 == 0:
            print(f"{mode}: step={step + 1} loss={losses[-1]:.6f}")
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    print(f"{mode}: elapsed_s={elapsed:.3f}")
    return RunResult(mode=mode, losses=losses, elapsed_s=elapsed, bad_step=bad_step)


def main() -> int:
    args = parse_args()
    seed_everything(0)

    print(json.dumps({
        "python": sys.version.split()[0],
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count(),
        "timm_version": getattr(timm, "__version__", "unknown"),
        "pretrained": args.pretrained,
        "mode": args.mode,
        "batch_size": args.batch_size,
        "image_size": args.image_size,
        "steps": args.steps,
        "warmup_steps": args.warmup_steps,
    }, sort_keys=True))

    if not torch.cuda.is_available():
        print("CUDA is required for this repro, but torch.cuda.is_available() is False.", file=sys.stderr)
        return 2

    torch.set_float32_matmul_precision("high")
    torch.backends.cudnn.benchmark = True

    device = torch.device("cuda")
    results: list[RunResult] = []

    if args.mode in {"eager", "both"}:
        results.append(
            train_one(
                build_model(args.pretrained, device, compiled=False),
                batch_size=args.batch_size,
                image_size=args.image_size,
                steps=args.steps,
                warmup_steps=args.warmup_steps,
                device=device,
                mode="eager",
            )
        )

    if args.mode in {"compiled", "both"}:
        results.append(
            train_one(
                build_model(args.pretrained, device, compiled=True),
                batch_size=args.batch_size,
                image_size=args.image_size,
                steps=args.steps,
                warmup_steps=args.warmup_steps,
                device=device,
                mode="compiled",
            )
        )

    summary = {
        result.mode: {
            "bad_step": result.bad_step,
            "losses": result.losses,
            "elapsed_s": result.elapsed_s,
        }
        for result in results
    }
    print(json.dumps(summary, sort_keys=True))

    compiled = next((r for r in results if r.mode == "compiled"), None)
    eager = next((r for r in results if r.mode == "eager"), None)
    if compiled and compiled.bad_step is not None:
        print("REPRODUCED: compiled TinyViT hit a non-finite loss.", file=sys.stderr)
        return 1
    if eager and eager.bad_step is not None:
        print("Eager run was also unstable here; the failure is not specific to torch.compile.", file=sys.stderr)
        return 1

    print("No non-finite loss observed in this environment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
