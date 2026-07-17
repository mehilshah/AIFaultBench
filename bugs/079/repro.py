#!/usr/bin/env python3
"""Reproduce the RegionViT local token embedding LayerNorm bug.

The failing path is `tokenize_local_3_conv=True`, where `nn.LayerNorm(init_dim)`
is applied directly to NCHW tensors. `LayerNorm` expects the normalized
dimension to be the last axis, so a forward pass fails on the first normalization
layer.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "vit_pytorch"))

from regionvit import RegionViT  # noqa: E402


def main() -> int:
    model = RegionViT(
        tokenize_local_3_conv=True,
        num_classes=10,
        window_size=7,
        local_patch_size=4,
    )
    model.eval()

    x = torch.randn(1, 3, 224, 224)
    print(f"input_shape={tuple(x.shape)}")

    try:
        y = model(x)
    except Exception as exc:  # pragma: no cover - intentional repro path
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        return 1

    print(f"output_shape={tuple(y.shape)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
