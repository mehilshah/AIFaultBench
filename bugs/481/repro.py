#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root / "codebase"))

    from jax import numpy as jnp
    from numpyro.distributions import WishartCholesky

    concentration = jnp.array([4.0, 5.0])
    scale_matrix = jnp.array([[[1.0, 0.5], [0.5, 1.0]]])

    try:
        result = WishartCholesky.infer_shapes(
            concentration, scale_matrix=scale_matrix
        )
    except TypeError as err:
        print("EXPECTED_EXCEPTION")
        print(type(err).__name__)
        print(err)
        if "Shapes must be 1D sequences" in str(err) or "unhashable type" in str(err):
            return 0
        return 1

    print("UNEXPECTED_SUCCESS")
    print(result)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
