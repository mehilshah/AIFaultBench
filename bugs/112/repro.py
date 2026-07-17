#!/usr/bin/env python3
"""Minimal reproduction for MotionBlur.direction_range."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

import albumentations as A  # noqa: E402


def main() -> None:
    np.set_printoptions(suppress=True)

    kernels: dict[int, np.ndarray] = {}
    for d in (-1, 0, 1):
        transform = A.MotionBlur(
            blur_limit=(5, 5),
            allow_shifted=False,
            angle_range=(0, 0),
            direction_range=(d, d),
            p=1.0,
        )
        kernel = transform.get_params()["kernel"]
        kernels[d] = kernel

        print(f"direction_range: {d}")
        print(kernel)
        print()

    identical = np.array_equal(kernels[-1], kernels[0]) and np.array_equal(kernels[0], kernels[1])
    print(f"kernels_all_equal: {identical}")


if __name__ == "__main__":
    main()
