#!/usr/bin/env python3
"""Minimal repro for the MPP dimension mismatch.

This loads the local source files directly so we only depend on the code that
participates in the failure, not optional package-root imports.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase" / "vit_pytorch"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vit_module = load_module("vit_module", CODEBASE / "vit.py")
mpp_module = load_module("mpp_module", CODEBASE / "mpp.py")

ViT = vit_module.ViT
MPP = mpp_module.MPP


def main() -> None:
    torch.manual_seed(0)

    model = ViT(
        image_size=256,
        patch_size=32,
        num_classes=1000,
        dim=1024,
        depth=6,
        heads=8,
        mlp_dim=2048,
        dropout=0.1,
        emb_dropout=0.1,
    )

    mpp_trainer = MPP(
        transformer=model,
        patch_size=32,
        dim=1024,
        mask_prob=0.15,
        random_patch_prob=0.30,
        replace_prob=0.50,
    )

    images = torch.FloatTensor(20, 3, 256, 256).uniform_(0.0, 1.0)
    print("running MPP forward pass", flush=True)
    loss = mpp_trainer(images)
    print(loss)


if __name__ == "__main__":
    main()
