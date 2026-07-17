#!/usr/bin/env python3
"""Minimal reproduction for the JAX gammaln subnormal regression."""

from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import numpy as np
import jax
import jax.numpy as jnp
import jax.scipy.special as jsp
import scipy
from scipy import special as sp_special


def main() -> int:
    x = jnp.asarray(
        np.asarray(
            [
                [-0.0, 0.0, np.float32(1.401298464324817e-45)],
                [-1.0, 1.0, np.float32(9.999999974752427e-07)],
            ],
            dtype=np.float32,
        )
    )

    actual = np.asarray(jsp.gammaln(x))
    expected = np.asarray(
        [
            [np.inf, np.inf, sp_special.gammaln(np.float32(1.401298464324817e-45))],
            [np.inf, 0.0, sp_special.gammaln(np.float32(9.999999974752427e-07))],
        ],
        dtype=np.float32,
    )

    print(f"jax: {jax.__version__}")
    print(f"jaxlib: {__import__('jaxlib').__version__}")
    print(f"numpy: {np.__version__}")
    print(f"scipy: {scipy.__version__}")
    print(f"actual: {actual.tolist()}")
    print(f"expected: {expected.tolist()}")

    if not np.isfinite(actual[0, 2]):
      raise AssertionError(
          "gammaln should be finite for the smallest positive float32 subnormal"
      )
    if not np.isclose(actual[0, 2], expected[0, 2], rtol=1e-6, atol=1e-6):
      raise AssertionError(
          f"unexpected value for subnormal input: {actual[0, 2]!r}"
      )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
