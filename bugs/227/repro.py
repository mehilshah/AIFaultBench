#!/usr/bin/env python3
"""Reproduce POT issue 229: ot.emd returns a higher-cost plan than a manual plan."""

from __future__ import annotations

import os
import sys

import numpy as np


def main() -> int:
    # POT 0.7.0 uses np.int inside the Cython wrapper, which no longer exists on
    # NumPy 1.24+. Add the legacy alias so we can exercise the actual solver.
    if not hasattr(np, "int"):
        np.int = int  # type: ignore[attr-defined]

    sys.path.insert(0, os.path.abspath("codebase"))

    import ot  # noqa: WPS433

    M = np.array(
        [
            [2.50275352e02, 3.74653218e02, 2.41352736e03, 1.00000000e32, 1.51751540e-03],
            [2.13082030e02, 3.28812836e02, 2.29487946e03, 1.00000000e32, 1.37109800e-01],
            [1.97333083e02, 3.09175848e02, 2.24250550e03, 1.00000000e32, 2.46506283e00],
            [1.00000000e32, 1.00000000e32, 1.00000000e32, 5.26223432e00, 2.50000000e31],
            [3.84690152e01, 8.09465684e01, 3.33064175e02, 2.50000000e31, 0.00000000e00],
        ],
        dtype=np.float64,
    )

    a = np.array([0.125, 0.125, 0.125, 0.125, 0.5], dtype=np.float64)
    b = np.array([0.125, 0.125, 0.125, 0.125, 0.5], dtype=np.float64)
    q = np.array(
        [
            [0, 0, 0, 0, 0.125],
            [0, 0, 0, 0, 0.125],
            [0, 0, 0, 0, 0.125],
            [0, 0, 0, 0.125, 0],
            [0.125, 0.125, 0.125, 0, 0.125],
        ],
        dtype=np.float64,
    )

    p = ot.emd(a=a, b=b, M=M, numItermax=2_000_000)
    p_cost = float(np.sum(p * M))
    q_cost = float(np.sum(q * M))

    print(f"POT version: {ot.__version__}")
    print("transport plan P:")
    print(p)
    print("row sums:", p.sum(axis=1))
    print("col sums:", p.sum(axis=0))
    print(f"P cost: {p_cost}")
    print(f"Q cost: {q_cost}")
    print(f"constraint rows exact: {(p.sum(axis=1) == a).all()}")
    print(f"constraint cols exact: {(p.sum(axis=0) == b).all()}")

    if not np.allclose(p.sum(axis=1), a) or not np.allclose(p.sum(axis=0), b):
        raise AssertionError("ot.emd returned an infeasible transport plan")

    if not (p_cost > q_cost):
        raise AssertionError("Expected ot.emd to return a higher-cost plan than Q")

    print("bug reproduced: ot.emd returns a feasible plan with cost above Q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
