#!/usr/bin/env python3
"""Minimal reproduction for JAX issue 38098."""

from __future__ import annotations

import numpy as np

import jax
import jax.numpy as jnp


def main() -> None:
  x = jnp.array([126.0], dtype=jnp.float32)
  fn = lambda x: jnp.sum(jnp.log2(jnp.exp2(x)))

  jit_result = np.asarray(jax.jit(jax.grad(fn))(x))
  eager_result = np.asarray(jax.grad(fn)(x))

  print(f"jax: {jax.__version__}")
  try:
    import jaxlib
    print(f"jaxlib: {jaxlib.__version__}")
  except Exception:
    pass
  print(f"x: {np.asarray(x)}")
  print(f"jit_result: {jit_result}")
  print(f"eager_result: {eager_result}")

  if not np.array_equal(jit_result, eager_result):
    raise AssertionError(
        "jit(grad(sum(log2(exp2(x))))) != eager grad: "
        f"jit_result={jit_result}, eager_result={eager_result}"
    )


if __name__ == "__main__":
  main()
