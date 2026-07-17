#!/usr/bin/env python3
import os
import sys
import warnings


def main() -> int:
  warnings.filterwarnings("ignore")
  os.environ.setdefault("JAX_PLATFORMS", "cpu")

  try:
    import numpy as np
    import jax.numpy as jnp
  except ImportError as exc:
    print(f"missing dep: {exc}")
    return 2

  x = np.array([np.nan, 0.0, -1.0], dtype=np.float32)
  x2 = np.array([1.0, 1.0, 1.0], dtype=np.float32)

  out = np.asarray(jnp.heaviside(jnp.asarray(x), jnp.asarray(x2)))
  expected = np.heaviside(x, x2)

  print("jax:", out.tolist())
  print("expected:", expected.tolist())

  # Match the bug report's exit convention:
  # return 0 when the bug is observed, 1 when JAX matches NumPy.
  if not np.allclose(out, expected, atol=1e-4, rtol=1e-3, equal_nan=True):
    return 0
  return 1


if __name__ == "__main__":
  sys.exit(main())
