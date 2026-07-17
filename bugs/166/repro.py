#!/usr/bin/env python3
"""Minimal reproduction for Kornia quaternion multiplication indexing bug."""

from __future__ import annotations

import os
import sys

import torch


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

from kornia.geometry.quaternion import Quaternion  # noqa: E402


def main() -> int:
    torch.manual_seed(42)

    x = Quaternion.random(3)
    a = x * x
    b = x[0] * x[0]
    c = x[[0, 0, 0]] * x
    d = x[[0, 1, 2]] * x

    print("torch:", torch.__version__)
    print("x[0]:", x[0])
    print("a[0]:", a[0])
    print("b   :", b)
    print("c[0]:", c[0])
    print("d[0]:", d[0])
    print("a[0] == b  :", torch.allclose(a[0].data, b.data))
    print("c[0] == d[0]:", torch.allclose(c[0].data, d[0].data))

    if not torch.allclose(c[0].data, d[0].data):
        raise SystemExit("reproduced: Quaternion.__mul__ gives different results for x[[0,0,0]] * x")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
