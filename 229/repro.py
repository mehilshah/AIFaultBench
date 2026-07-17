#!/usr/bin/env python3
"""Minimal reproduction for POT issue #738."""

from __future__ import annotations

import sys

import numpy as np
import ot


def main() -> int:
    sample1 = np.array([0.1, 0.11, 0.4, 0.6])
    sample2 = np.array([0.21, 0.15, 0.7, 0.95])
    delta = 0.02

    d1 = ot.wasserstein_circle(sample1, sample2)
    d1_p2 = ot.wasserstein_circle(sample1, sample2, p=2)
    d2 = ot.wasserstein_circle(sample1 + delta, sample2 + delta)
    d3 = ot.wasserstein_circle((sample1 + delta) % 1, (sample2 + delta) % 1)
    d2_p2 = ot.wasserstein_circle(sample1 + delta, sample2 + delta, p=2)

    print(f"sample1 = {sample1.tolist()}")
    print(f"sample2 = {sample2.tolist()}")
    print(f"delta = {delta}")
    print(f"p=1, original   = {d1.tolist()}")
    print(f"p=2, original   = {d1_p2.tolist()}")
    print(f"p=1, shifted    = {d2.tolist()}")
    print(f"p=1, shifted %1  = {d3.tolist()}")
    print(f"p=2, shifted    = {d2_p2.tolist()}")
    print(f"p=1 abs diff    = {float(np.abs(d1 - d2)[0])}")
    print(f"p=1 abs diff %1 = {float(np.abs(d1 - d3)[0])}")
    print(f"p=2 abs diff    = {float(np.abs(d1_p2 - d2_p2)[0])}")

    if np.allclose(d1, d2):
        print("unexpected: p=1 result stayed invariant under a shared shift", file=sys.stderr)
        return 0

    print(
        "bug reproduced: p=1 distance changes under a shared shift; "
        "the report's equality assertion fails",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
