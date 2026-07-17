from __future__ import annotations

import math

import jax
import jax.numpy as jnp


def compute(x: jnp.ndarray) -> tuple[float, float]:
  fn = lambda y: jnp.log2(jnp.exp2(y))
  jit_value = float(jax.jit(fn)(x))
  eager_value = float(fn(x))
  return jit_value, eager_value


def main() -> None:
  print(f"jax={jax.__version__}")
  print(f"jaxlib={__import__('jaxlib').__version__}")

  x1 = jnp.array(128.0, dtype=jnp.float32)
  jit1, eager1 = compute(x1)
  print(f"x=128.0 jit={jit1} eager={eager1}")

  x2 = jnp.array(13.0, dtype=jnp.float32)
  jit2, eager2 = compute(x2)
  print(f"x=13.0 jit={jit2} eager={eager2}")

  if not (jit1 == 128.0 and math.isinf(eager1)):
    raise SystemExit("unexpected result for x=128.0")
  if not (jit2 == 13.0 and eager2 == 13.000000953674316):
    raise SystemExit("unexpected result for x=13.0")

  print("BUG REPRODUCED: jit(log2(exp2(x))) returns x and masks overflow/rounding.")


if __name__ == "__main__":
  main()
