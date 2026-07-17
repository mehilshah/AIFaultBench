"""Compatibility aliases for the bundled POT snapshot.

The source snapshot targets older SciPy and NumPy releases.  These aliases
allow the local repro to import the package on modern versions without
modifying the application code.
"""

from __future__ import annotations


def apply() -> None:
    import numpy as np
    import scipy.optimize

    if not hasattr(np, "infty"):
        np.infty = np.inf

    if not hasattr(scipy.optimize.linesearch, "scalar_search_armijo"):
        from scipy.optimize._linesearch import scalar_search_armijo

        scipy.optimize.linesearch.scalar_search_armijo = scalar_search_armijo
