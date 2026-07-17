import os

import numpy as np

# Compatibility shims for the older POT codebase on modern NumPy/SciPy.
np.infty = np.inf

import scipy.optimize
import scipy.optimize._linesearch as _linesearch

scipy.optimize.linesearch.scalar_search_armijo = _linesearch.scalar_search_armijo

import ot


def main() -> None:
    n = int(os.environ.get("N", "50000"))
    print(f"allocating M {n} x {n}", flush=True)
    M = np.zeros((n, n), dtype=np.float64)
    print("calling ot.emd([], [], M)", flush=True)
    G = ot.emd([], [], M)
    print(f"success: {G.shape} sum={G.sum()}", flush=True)


if __name__ == "__main__":
    main()
