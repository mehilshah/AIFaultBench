#!/usr/bin/env python3
"""Reproduce the JAX `jit(grad(f))` vs `grad(f)` mismatch.

The bug report describes a float32 boundary case where XLA simplification
changes the gradient result for:

    sqrt(abs(square(x)))

at the smallest normal float32.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import jax
import jax.numpy as jnp


ROOT = Path(__file__).resolve().parent


def program(x: jnp.ndarray) -> jnp.ndarray:
    return jnp.sqrt(jnp.abs(jnp.square(x)))


def main() -> int:
    x = jnp.array([1.1754944e-38], dtype=jnp.float32)

    jit_result = np.asarray(jax.jit(jax.grad(lambda y: jnp.sum(program(y))))(x))
    eager_result = np.asarray(jax.grad(lambda y: jnp.sum(program(y)))(x))

    payload = {
        "jax_version": getattr(jax, "__version__", "unknown"),
        "jaxlib_version": __import__("jaxlib").__version__,
        "input": x.tolist(),
        "dtype": str(x.dtype),
        "jit_grad": jit_result.tolist(),
        "eager_grad": eager_result.tolist(),
        "allclose": bool(np.allclose(jit_result, eager_result, rtol=1e-5, atol=1e-5)),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if payload["allclose"]:
        print("No reproduction: jit(grad(f)) matches grad(f).")
        return 0

    print("BUG REPRODUCED: jit(grad(f)) != grad(f) for sqrt(abs(square(x))).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
