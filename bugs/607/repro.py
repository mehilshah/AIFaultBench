from __future__ import annotations

import numpy as np

import jax
import jax.numpy as jnp
import jaxlib


def main() -> None:
  jax.config.update("jax_enable_x64", True)

  x = np.array([
      -3.4028235e+38, -3.4028235e+38, 3.4028235e+38, 1.0,
      1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 3.4028235e+38, 1.0,
      1.0, 1.0, 1.0, 1.0,
  ], dtype=np.float32)

  np_std = np.std(x)
  jnp_std = float(jnp.std(jnp.array(x)))

  print(f"numpy.std(x) = {np_std!r}")
  print(f"jax.std(x)   = {jnp_std!r}")
  print(f"jax.__version__ = {jax.__version__}")
  print(f"jaxlib.__version__ = {jaxlib.__version__}")
  print(f"reproduced = {np.isnan(np_std) and np.isinf(jnp_std)}")


if __name__ == "__main__":
  main()
