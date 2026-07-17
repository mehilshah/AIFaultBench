#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
if str(CODEBASE) not in sys.path:
  sys.path.insert(0, str(CODEBASE))

# Force CPU execution so the repro stays stable across machines.
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import jax
import jax.numpy as jnp
import jaxlib


def f(x: jnp.ndarray) -> jnp.ndarray:
  return jnp.sum(jnp.log(jnp.exp(x)))


def run_case(value: float) -> tuple[np.ndarray, np.ndarray]:
  x = jnp.array([value], dtype=jnp.float32)
  jit_out = np.asarray(jax.jit(jax.grad(f))(x))
  eager_out = np.asarray(jax.grad(f)(x))
  print(f"x={value:g} jit: {jit_out} eager: {eager_out}")
  return jit_out, eager_out


def main() -> int:
  print(f"jax={jax.__version__}")
  print(f"jaxlib={jaxlib.__version__}")
  print(f"numpy={np.__version__}")

  observed = {
      89.0: run_case(89.0),
      88.0: run_case(88.0),
  }

  assert np.array_equal(observed[89.0][0], np.array([1.0], dtype=np.float32))
  assert np.array_equal(observed[88.0][0], np.array([1.0], dtype=np.float32))
  assert np.isnan(observed[89.0][1]).all()
  assert np.array_equal(observed[88.0][1], np.array([0.0], dtype=np.float32))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
