#!/usr/bin/env python3
"""Minimal JAX repro for `isinstance(x, ArrayLike)` on traced values."""

import jax
from jax import Array
from jax.typing import ArrayLike


def f(x):
  array_check = isinstance(x, Array)
  arraylike_check = isinstance(x, ArrayLike)
  print(x, array_check, arraylike_check)


def main():
  jax.jit(f)(0)
  jax.print_environment_info()


if __name__ == "__main__":
  main()
