#!/usr/bin/env python3

"""Minimal repro for the NumPyro import failure with JAX 0.10.0."""

from __future__ import annotations


def main() -> int:
    import jax
    import jax.extend.core.primitives as primitives

    print(f"jax_version={jax.__version__}")
    print(f"has_xla_pmap_p={hasattr(primitives, 'xla_pmap_p')}")

    import numpyro

    print(f"numpyro_version={numpyro.__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
