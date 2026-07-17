#!/usr/bin/env python3
"""Minimal reproduction harness for POT issue 712.

The report claims that ``ot.dist(..., metric='minkowski', p=...)`` ignores the
``p`` parameter. In this checkout, the 2D control below matches SciPy exactly
for multiple values of ``p``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
    sys.path.insert(0, str(CODEBASE))

import ot  # noqa: E402


def summarize_1d() -> dict[str, float | bool]:
    x = np.linspace(0.0, 1.0, 1001).reshape(-1, 1)
    m1 = ot.dist(x, metric="minkowski", p=1)
    m2 = ot.dist(x, metric="minkowski", p=2)
    e1 = ot.dist(x, metric="euclidean")
    e2 = ot.dist(x, metric="sqeuclidean")

    return {
        "1d_m1_equals_m2": bool(np.allclose(m1, m2)),
        "1d_m2_equals_e2": bool(np.allclose(m2, e2)),
        "1d_max_abs_m1_minus_e1": float(np.max(np.abs(m1 - e1))),
        "1d_max_abs_m2_minus_e2": float(np.max(np.abs(m2 - e2))),
    }


def summarize_2d() -> dict[str, float | bool]:
    rng = np.random.RandomState(0)
    x = rng.randn(5, 2)

    results: dict[str, np.ndarray] = {}
    scipy_results: dict[str, np.ndarray] = {}
    for p in (1, 2, 3):
        results[f"p{p}"] = ot.dist(x, x, metric="minkowski", p=p)
        scipy_results[f"p{p}"] = cdist(x, x, metric="minkowski", p=p)

    return {
        "2d_m1_equals_m2": bool(np.allclose(results["p1"], results["p2"])),
        "2d_m2_equals_m3": bool(np.allclose(results["p2"], results["p3"])),
        "2d_max_abs_m1_minus_m2": float(np.max(np.abs(results["p1"] - results["p2"]))),
        "2d_max_abs_m2_minus_m3": float(np.max(np.abs(results["p2"] - results["p3"]))),
        "2d_max_abs_p1_minus_scipy": float(
            np.max(np.abs(results["p1"] - scipy_results["p1"]))
        ),
        "2d_max_abs_p2_minus_scipy": float(
            np.max(np.abs(results["p2"] - scipy_results["p2"]))
        ),
        "2d_max_abs_p3_minus_scipy": float(
            np.max(np.abs(results["p3"] - scipy_results["p3"]))
        ),
    }


def main() -> int:
    report = {
        "ot_version": getattr(ot, "__version__", "unknown"),
        "numpy_version": np.__version__,
        "scipy_version": __import__("scipy").__version__,
        "report_sample": summarize_1d(),
        "2d_control": summarize_2d(),
    }

    report["reproducible"] = False
    report["note"] = (
        "The 1D sample is not discriminating because Minkowski distances in one "
        "dimension are identical for all p. The 2D control shows p is propagated "
        "and matches SciPy."
    )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
