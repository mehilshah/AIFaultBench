#!/usr/bin/env python3
import os
import sys
import warnings


def main() -> int:
  warnings.filterwarnings("ignore")
  os.environ.setdefault("JAX_PLATFORMS", "cpu")

  try:
    import numpy as np
    import jax
    import jax.numpy as jnp
    import jax.scipy.special as jsp
    import jaxlib
  except ImportError as exc:
    print(f"missing dep: {exc}")
    return 2

  a = np.array([np.inf], dtype=np.float32)
  x = np.array([2.0], dtype=np.float32)
  expected = np.array([1.0], dtype=np.float32)
  out = np.asarray(jsp.gammaincc(jnp.asarray(a), jnp.asarray(x)))

  print(f"jax={jax.__version__}")
  print(f"jaxlib={jaxlib.__version__}")
  print("jax:", out.tolist())
  print("expected:", expected.tolist())

  if not np.array_equal(out, expected, equal_nan=True):
    print("BUG REPRODUCED: gammaincc(inf, 2.0) != 1.0")
    return 0

  print("BUG NOT REPRODUCED: current environment returns the expected value")
  return 1


if __name__ == "__main__":
  raise SystemExit(main())
