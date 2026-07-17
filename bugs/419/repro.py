#!/usr/bin/env python3
"""Minimal reproducer for jax.scipy.stats.chi2.logpdf boundary handling."""

from __future__ import annotations

import sys

import numpy as np
import scipy.stats

import jax
import jax.numpy as jnp
import jax.scipy.stats


def _format_value(value: object) -> str:
  arr = np.asarray(value)
  if arr.shape == ():
    return repr(arr.item())
  return repr(arr)


def _matches(expected: object, actual: object) -> bool:
  expected_arr = np.asarray(expected)
  actual_arr = np.asarray(actual)
  if expected_arr.shape != actual_arr.shape:
    return False
  return np.array_equal(expected_arr, actual_arr, equal_nan=True)


def main() -> int:
  jax.config.update("jax_enable_x64", True)

  cases = [
      (np.float32(0.0), np.float32(2.0)),
      (np.float64(0.0), np.float64(2.0)),
      (np.float32(np.inf), np.float32(2.0)),
  ]

  print(f"jax version: {jax.__version__}")
  print(f"scipy version: {scipy.__version__}")
  print()

  mismatches = 0
  for x, df in cases:
    scipy_value = scipy.stats.chi2.logpdf(np.array(x), np.array(df))
    jax_value = jax.scipy.stats.chi2.logpdf(jnp.array(x), jnp.array(df))
    jit_value = jax.jit(
        lambda a, b: jax.scipy.stats.chi2.logpdf(a, b)
    )(jnp.array(x), jnp.array(df))

    print(f"x = {x!r}, df = {df!r}")
    print(f"  scipy: {_format_value(scipy_value)}")
    print(f"  jax:   {_format_value(jax_value)}")
    print(f"  jit:   {_format_value(jit_value)}")

    if not (
        _matches(scipy_value, jax_value) and _matches(scipy_value, jit_value)
    ):
      mismatches += 1
      print("  status: MISMATCH")
    else:
      print("  status: OK")
    print()

  if mismatches:
    print(f"Detected {mismatches} mismatch(es).", file=sys.stderr)
    return 1

  print("No mismatch detected.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
