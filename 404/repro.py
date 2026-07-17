#!/usr/bin/env python3
"""Minimal repro for JAX Poisson CDF boundary handling."""

from __future__ import annotations

import math

import numpy as np
import scipy.stats

import jax
import jax.numpy as jnp
import jax.scipy.stats


jax.config.update("jax_enable_x64", True)


CASES = [
    (np.float32(np.inf), np.float32(0.0), np.float32(0.0)),
    (np.float32(np.inf), np.float32(1.0), np.float32(0.0)),
    (np.float32(np.inf), np.float32(2.0), np.float32(0.0)),
    (np.float32(np.inf), np.float32(1.0), np.float32(1.0)),
    (np.float32(-np.inf), np.float32(1.0), np.float32(0.0)),
    (np.float32(np.nan), np.float32(1.0), np.float32(0.0)),
    (np.float32(-1.0), np.float32(1.0), np.float32(0.0)),
    (np.float32(0.0), np.float32(0.0), np.float32(0.0)),
    (np.float32(0.0), np.float32(1.0), np.float32(0.0)),
    (np.float32(1.0), np.float32(1.0), np.float32(0.0)),
    (np.float32(2.0), np.float32(1.0), np.float32(0.0)),
    (np.float32(0.5), np.float32(1.0), np.float32(0.0)),
]


def _scalar(x):
  return np.asarray(x).item()


def _same_nan(a, b):
  return math.isnan(a) and math.isnan(b)


def main() -> int:
  reproduced = False
  for k, mu, loc in CASES:
    scipy_result = scipy.stats.poisson.cdf(np.array(k), np.array(mu), loc=np.array(loc))
    jax_result = jax.scipy.stats.poisson.cdf(jnp.array(k), jnp.array(mu), jnp.array(loc))
    jit_result = jax.jit(
        lambda k_, mu_, loc_: jax.scipy.stats.poisson.cdf(k_, mu_, loc_)
    )(jnp.array(k), jnp.array(mu), jnp.array(loc))

    scipy_scalar = _scalar(scipy_result)
    jax_scalar = _scalar(jax_result)
    jit_scalar = _scalar(jit_result)

    print(f"k={k!r}, mu={mu!r}, loc={loc!r}")
    print(f"  scipy: {scipy_scalar}")
    print(f"  jax:   {jax_scalar}")
    print(f"  jit:   {jit_scalar}")
    print()

    if (
        np.isinf(k)
        and k > 0
        and mu > 0
        and scipy_scalar == 1.0
        and _same_nan(jax_scalar, jit_scalar)
    ):
      reproduced = True

  if reproduced:
    print("BUG REPRODUCED: jax.scipy.stats.poisson.cdf(k=+inf, mu>0) returns nan")
    return 0

  print("BUG NOT REPRODUCED")
  return 1


if __name__ == "__main__":
  raise SystemExit(main())
