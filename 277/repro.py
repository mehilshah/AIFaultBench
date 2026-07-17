#!/usr/bin/env python3
"""Minimal reproduction for Poisson dtype-dependent log_prob behavior."""

from __future__ import annotations

import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "codebase"))

import jax.numpy as jnp
import numpyro.distributions as dist


def main() -> None:
    value = 1.999999
    int_rate = dist.Poisson(2)
    float_rate = dist.Poisson(2.0)

    int_log_prob = int_rate.log_prob(value)
    float_log_prob = float_rate.log_prob(value)

    print(f"value={value}")
    print(f"int_rate dtype={jnp.asarray(int_rate.rate).dtype}, rate={int_rate.rate}")
    print(
        f"float_rate dtype={jnp.asarray(float_rate.rate).dtype}, rate={float_rate.rate}"
    )
    print(f"Poisson(2).log_prob({value}) = {int_log_prob}")
    print(f"Poisson(2.0).log_prob({value}) = {float_log_prob}")
    print(f"absolute_difference = {jnp.abs(int_log_prob - float_log_prob)}")

    # The bug is the dtype-sensitive branch: the same value gets different
    # results depending on whether the constructor saw an int or a float rate.
    assert float(jnp.abs(int_log_prob - float_log_prob)) > 0.1


if __name__ == "__main__":
    main()
