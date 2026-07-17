#!/usr/bin/env python3
"""Minimal reproducer for jax.nn.scaled_matmul on CPU."""

from __future__ import annotations

import os
import sys
import traceback


def main() -> int:
  root = os.path.dirname(os.path.abspath(__file__))
  sys.path.insert(0, os.path.join(root, "codebase"))
  os.environ.setdefault("JAX_PLATFORMS", "cpu")

  import jax  # noqa: WPS433
  import jax.numpy as jnp  # noqa: WPS433

  print(f"jax={jax.__version__}")
  print(f"jaxlib={jax.lib.__version__}")
  print(f"devices={jax.devices()}")

  key = jax.random.PRNGKey(0)
  x = jax.random.normal(key, [3, 16, 16], dtype=jnp.bfloat16)
  print(f"input_dtype={x.dtype}, input_shape={x.shape}")

  try:
    out = jax.nn.scaled_matmul(x, x, x, x)
  except Exception:  # noqa: BLE001
    traceback.print_exc()
    return 1

  print(f"unexpected_success={out.shape} {out.dtype}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
