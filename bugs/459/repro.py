#!/usr/bin/env python3
"""Minimal reproducer for NumPyro issue 2064."""

from __future__ import annotations

import sys
import traceback

import jax
import numpyro
from numpyro.infer.inspect import get_model_relations


def guide():
    numpyro.param("p", lambda _: 1.0)


def main() -> int:
    print(f"jax={jax.__version__} numpyro={numpyro.__version__}")
    try:
        get_model_relations(guide)
    except TypeError as exc:
        traceback.print_exc()
        print(f"REPRODUCED: {type(exc).__name__}: {exc}")
        return 0
    raise AssertionError(
        "Expected get_model_relations(guide) to fail for lambda-valued params."
    )


if __name__ == "__main__":
    sys.exit(main())
