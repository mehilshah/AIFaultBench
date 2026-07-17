#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

import numpy as np


REPO_ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "codebase"))


def main() -> None:
  import jax
  import jax.numpy as jnp

  try:
    import jaxlib
    jaxlib_version = jaxlib.__version__
  except Exception as exc:  # pragma: no cover - defensive logging only.
    jaxlib_version = f"unavailable ({exc})"

  x = jnp.array(89.0, dtype=jnp.float32)
  jit_fn = jax.jit(lambda value: jnp.log(jnp.exp(value)))
  jit_result = jit_fn(x)
  eager_result = jnp.log(jnp.exp(x))

  print(f"jax: {jax.__version__}")
  print(f"jaxlib: {jaxlib_version}")
  print(f"backend: {jax.default_backend()}")
  print(f"jit(log(exp(89))) = {float(jit_result)}")
  print(f"eager log(exp(89)) = {float(eager_result)}")
  print(f"jit array repr = {np.asarray(jit_result)!r}")
  print(f"eager array repr = {np.asarray(eager_result)!r}")

  np.testing.assert_array_equal(
      np.asarray(jit_result),
      np.asarray(eager_result),
      err_msg=(
          f"jit(log(exp(89.0))) = {float(jit_result)} but "
          f"eager = {float(eager_result)}: JIT hides exp overflow"
      ),
  )


if __name__ == "__main__":
  main()
