"""Minimal repro for the JAX 0.6.0 and Haiku compatibility break."""

from __future__ import annotations

import traceback

import jax


def main() -> None:
    print(f"jax={jax.__version__}")
    try:
        import haiku as hk

        print(f"haiku={hk.__version__}")
        print("import succeeded")
    except Exception:
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
