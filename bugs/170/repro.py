#!/usr/bin/env python3
"""Minimal reproduction for RandomThinPlateSpline same_on_batch regression."""

from __future__ import annotations

import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from kornia.augmentation import RandomThinPlateSpline  # noqa: E402


def main() -> int:
    torch.manual_seed(42)
    x = torch.randn(4, 3, 32, 32)

    aug = RandomThinPlateSpline(p=1.0, same_on_batch=True)
    _ = aug(x)
    params = aug._params
    src = params["src"]
    dst = params["dst"]

    src_equal = torch.allclose(src[0], src[1])
    dst_equal = torch.allclose(dst[0], dst[1])

    print(f"src_equal={src_equal}")
    print(f"dst_equal={dst_equal}")
    print(f"src_shape={tuple(src.shape)}")
    print(f"dst_shape={tuple(dst.shape)}")

    # This is the contract users expect from same_on_batch=True.
    assert dst_equal, "RandomThinPlateSpline should reuse identical TPS control points across the batch"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
