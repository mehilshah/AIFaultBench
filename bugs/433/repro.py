#!/usr/bin/env python3
"""Minimal reproduction for JAX ShapeDtypeStruct serialization."""

from __future__ import annotations

import os
import tempfile

import jax
import jax.numpy as jnp
import numpy as np


def main() -> None:
    x = jax.ShapeDtypeStruct((10, 10), jnp.float16)

    fd, path = tempfile.mkstemp(suffix=".npy")
    os.close(fd)
    try:
        np.save(path, x)
        y = jnp.load(path, allow_pickle=True)

        print(f"saved: {x!r}")
        print(f"loaded_type: {type(y).__name__}")
        print(f"loaded_shape: {getattr(y, 'shape', None)!r}")
        print(f"loaded_dtype: {getattr(y, 'dtype', None)!r}")
        print(f"loaded_repr: {y!r}")

        if isinstance(y, np.ndarray) and y.shape == () and y.dtype == object:
            print(f"wrapped_value_type: {type(y.item()).__name__}")
            print(f"wrapped_value_repr: {y.item()!r}")
            print("result: reproduced")
        else:
            print("result: not reproduced")
    finally:
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    main()
