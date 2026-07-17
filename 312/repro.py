#!/usr/bin/env python3
"""Reproduce POT issue 82 with the original distance matrices."""

from __future__ import annotations

import pathlib
import sys
import traceback

import numpy as np


def _patch_compatibility() -> None:
    # POT 0.5.1 expects an older SciPy API and NumPy symbol.
    np.infty = np.inf  # type: ignore[attr-defined]

    import scipy.optimize.linesearch as linesearch

    try:
        from scipy.optimize._linesearch import scalar_search_armijo
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise RuntimeError("could not import scalar_search_armijo shim") from exc

    linesearch.scalar_search_armijo = scalar_search_armijo


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "codebase"))

    _patch_compatibility()

    import ot  # noqa: WPS433

    dists0 = np.loadtxt(root / "dists0.txt", dtype=float)
    dists1 = np.loadtxt(root / "dists1.txt", dtype=float)
    p = ot.unif(dists0.shape[0])
    q = ot.unif(dists1.shape[0])

    print(f"dists0 shape: {dists0.shape}")
    print(f"dists1 shape: {dists1.shape}")
    print(f"max abs diff: {np.max(np.abs(dists0 - dists1)):.6f}")

    same = ot.gromov.gromov_wasserstein(
        dists1, dists1, p, q, "square_loss", verbose=False, log=True
    )
    print(f"same-matrix call succeeded: {same[0].shape}")

    try:
        ot.gromov.gromov_wasserstein(
            dists0, dists1, p, q, "square_loss", verbose=False, log=True
        )
    except Exception as exc:
        print(f"reproduced exception: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 1

    print("unexpected success for the slightly different matrices")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
