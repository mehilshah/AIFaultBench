#!/usr/bin/env python3
"""Reproduce POT issue 229: ot.emd returns a feasible but suboptimal plan."""

from __future__ import annotations

import os
import sys
import types

import numpy as np


def _install_numpy_compat_shims() -> None:
    """Restore aliases removed by newer NumPy releases for this legacy codebase."""
    if not hasattr(np, "int"):
        np.int = int  # type: ignore[attr-defined]
    if not hasattr(np, "infty"):
        np.infty = np.inf  # type: ignore[attr-defined]


def _install_scipy_compat_shim() -> None:
    """Provide the legacy scipy.optimize.linesearch module expected by POT 0.7.0."""
    import scipy.optimize

    try:
        from scipy.optimize import _linesearch
    except Exception as exc:  # pragma: no cover - environment specific
        raise RuntimeError("SciPy does not expose _linesearch; cannot shim POT import") from exc

    legacy_module = sys.modules.get("scipy.optimize.linesearch")
    if legacy_module is None:
        legacy_module = types.ModuleType("scipy.optimize.linesearch")

    legacy_module.scalar_search_armijo = _linesearch.scalar_search_armijo
    sys.modules["scipy.optimize.linesearch"] = legacy_module
    scipy.optimize.linesearch = legacy_module  # type: ignore[attr-defined]


def main() -> int:
    _install_numpy_compat_shims()
    _install_scipy_compat_shim()

    repo_root = os.path.abspath(os.path.dirname(__file__))
    codebase_path = os.path.join(repo_root, "codebase")
    if codebase_path not in sys.path:
        sys.path.insert(0, codebase_path)

    import ot

    m = np.array(
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

    p, log = ot.emd(a=a, b=b, M=m, numItermax=2_000_000, log=True)
    cost_p = float(log["cost"])
    cost_q = float(np.sum(q * m))
    row_sums = p.sum(axis=1)
    col_sums = p.sum(axis=0)

    print("ot version:", ot.__version__)
    print("transport plan P:\n", p)
    print("row sums:", row_sums)
    print("col sums:", col_sums)
    print("P cost:", cost_p)
    print("Q cost:", cost_q)
    print("P equals Q:", np.allclose(p, q))
    print("marginals exact:", np.all(p.sum(axis=1) == a) and np.all(p.sum(axis=0) == b))
    print("warning:", log["warning"])

    if not np.allclose(p.sum(axis=1), a) or not np.allclose(p.sum(axis=0), b):
        raise AssertionError("emd returned an infeasible plan")

    if not (cost_p > cost_q + 1e-9):
        raise AssertionError(
            f"expected the reported bug, but got cost_p={cost_p} <= cost_q={cost_q}"
        )

    raise AssertionError(
        "BUG REPRODUCED: ot.emd returned a feasible but suboptimal plan "
        f"(cost {cost_p} vs reference {cost_q})"
    )


if __name__ == "__main__":
    raise SystemExit(main())
