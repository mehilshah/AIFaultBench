import numpy as np

import jax
import jax.numpy as jnp


def main() -> None:
  jax.config.update("jax_enable_x64", True)

  x = np.array([-1, 1], dtype=np.int32)
  expected = np.cumsum(x, dtype=bool)
  actual = np.asarray(jnp.cumsum(jnp.array(x), dtype=bool))

  print("jax_version:", jax.__version__)
  print("jaxlib_version:", jax.lib.__version__)
  print("numpy_version:", np.__version__)
  print("input:", x.tolist(), x.dtype)
  print("expected_numpy:", expected.tolist(), expected.dtype)
  print("actual_jax:", actual.tolist(), actual.dtype)
  print("matches:", bool(np.array_equal(expected, actual)))


if __name__ == "__main__":
  main()
