import sys
import traceback

import jax
import equinox as eqx


class Problematic(eqx.Module):
    nested: dict

    def __init__(self, nested):
        self.nested = nested

    def __call__(self):
        return 1.0


def merge(parameters, static):
    return eqx.combine(parameters, static)()


def main():
    print(f"Python:  {sys.version}")
    print(f"Equinox: {eqx.__version__}")
    print(f"JAX:     {jax.__version__}")

    model = Problematic({0: 0.0})
    print(f"Model:   {model!r}")

    try:
        print(f"hash(model) = {hash(model)}")
    except Exception as exc:
        print(f"hash(model) failed: {type(exc).__name__}: {exc}")

    arr, static = eqx.partition(model, eqx.is_array)
    print(f"partitioned arr = {arr!r}")
    print(f"partitioned static = {static!r}")

    try:
        out = jax.jit(merge, static_argnames="static")(arr, static)
    except Exception as exc:
        print(f"jax.jit(..., static_argnames='static') failed: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        return 0

    print(f"jax.jit output = {out!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
