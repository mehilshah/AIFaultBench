#!/usr/bin/env python3
"""Minimal reproduction for POT issue 418.

This reproduces the sliced Wasserstein normalization bug when a custom
projection matrix is passed in. The script also applies small runtime
compatibility shims so the older POT codebase imports on the current
NumPy/SciPy stack without touching application code.
"""

from __future__ import annotations

import numpy as np


def _install_runtime_shims() -> None:
    """Restore small APIs that this codebase expects at import time."""

    # POT 0.8.x still references np.infty, which was removed in NumPy 2.
    if not hasattr(np, "infty"):
        np.infty = np.inf  # type: ignore[attr-defined]

    # POT imports scalar_search_armijo from scipy.optimize or the legacy
    # scipy.optimize.linesearch location. Newer SciPy versions removed it.
    import scipy.optimize
    import scipy.optimize.linesearch as linesearch

    def scalar_search_armijo(*args, **kwargs):
        # This repro does not exercise the line-search path; we only need the
        # symbol to exist so importing ot succeeds.
        return None, None

    scipy.optimize.scalar_search_armijo = scalar_search_armijo
    linesearch.scalar_search_armijo = scalar_search_armijo


def main() -> int:
    _install_runtime_shims()

    import ot

    n_projections = 10
    seed = 12
    X = np.array([[1, 2], [4, 5], [6, -8]], dtype=float)
    Y = np.array([[0, 2], [14, 52], [3, -12]], dtype=float)

    cost1, log1 = ot.sliced.sliced_wasserstein_distance(
        X, Y, seed=seed, n_projections=n_projections, log=True
    )
    P = ot.sliced.get_random_projections(X.shape[1], n_projections=10, seed=seed)
    cost2, log2 = ot.sliced.sliced_wasserstein_distance(
        X, Y, projections=P, log=True
    )

    proj_diff = float(np.linalg.norm(log1["projections"] - log2["projections"]))
    emd_sum = float(np.sum(log2["projected_emds"]))
    expected_true = float((emd_sum / n_projections) ** 0.5)
    expected_default = float((emd_sum / 50) ** 0.5)
    delta = float(abs(cost1 - cost2))

    print(f"projections_equal_norm={proj_diff:.12f}")
    print(f"cost_with_seed={cost1:.15f}")
    print(f"cost_with_custom_projections={cost2:.15f}")
    print(f"absolute_delta={delta:.15f}")
    print(f"projection_count={log2['projections'].shape[1]}")
    print(f"emd_sum={emd_sum:.15f}")
    print(f"expected_using_10_projections={expected_true:.15f}")
    print(f"expected_using_default_50={expected_default:.15f}")

    if proj_diff != 0.0:
        raise AssertionError("The custom projection matrix should match the seeded projections.")
    if not np.isclose(cost1, expected_true):
        raise AssertionError("Seeded result does not match the expected normalization.")
    if not np.isclose(cost2, expected_default):
        raise AssertionError("Custom projection result does not match the buggy normalization.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
