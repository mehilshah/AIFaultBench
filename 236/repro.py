import sys
import traceback

import jax
import jax.numpy as jnp
import numpy as np

import equinox as eqx


class MyArray:
    def __init__(self, x):
        self.x = x

    def __array__(self, dtype=None, copy=None) -> np.ndarray:
        return np.asarray(self.x, dtype=dtype)


class MyEqxArray(eqx.Module):
    x: jax.Array

    def __array__(self, dtype=None, copy=None) -> np.ndarray:
        return np.asarray(self.x, dtype=dtype)


def main() -> int:
    print(f"jax={jax.__version__}")
    print(f"equinox={getattr(eqx, '__version__', 'unknown')}")

    x = MyArray(jnp.array([1, 2, 3]))
    print("plain_class_asarray=", jnp.asarray(x), sep="")

    y = MyEqxArray(jnp.array([1, 2, 3]))
    try:
        result = jnp.asarray(y)
    except TypeError as exc:
        print("bug_reproduced=True")
        print(f"exception_type={type(exc).__name__}")
        print(f"exception_message={exc}")
        traceback.print_exc()
        return 0

    print("bug_reproduced=False")
    print(f"unexpected_result={result}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
