from __future__ import annotations

import equinox as eqx
import jax
import jax.numpy as jnp


def main() -> int:
    @eqx.filter_jit
    def foo(x):
        return eqx.error_if(x, x > 0.0, "my message")

    print(f"equinox={eqx.__version__}")
    print(f"jax={jax.__version__}")

    foo(jnp.array(-1.0))
    print("first_call=ok")

    try:
        foo(jnp.array(1.0))
    except Exception as exc:  # noqa: BLE001 - we want the actual runtime type
        print(f"second_call_exception={type(exc).__name__}")
        print(f"second_call_message={exc}")
        if type(exc).__name__ == "ValueError":
            print("bug_reproduced=true")
            return 0
        print("bug_reproduced=false")
        return 1

    print("bug_reproduced=false")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
