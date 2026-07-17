from __future__ import annotations

from typing import Optional, Union

import jax.numpy as jnp
from jaxtyping import Int, jaxtyped
from typeguard import typechecked as typechecker


@jaxtyped(typechecker=typechecker)
def with_optional(x: Optional[Int[jnp.ndarray, " N"]]) -> int:
    return 1


@jaxtyped(typechecker=typechecker)
def with_union(x: Union[Int[jnp.ndarray, " N"], None]) -> int:
    return 2


@jaxtyped(typechecker=typechecker)
def with_pipe(x: Int[jnp.ndarray, " N"] | None) -> int:
    return 3


def _expect_reject(name: str, fn, value) -> None:
    try:
        fn(value)
    except Exception as exc:
        print(f"{name}: rejected bad dtype ({type(exc).__name__})")
    else:
        raise AssertionError(f"{name} unexpectedly accepted the bad dtype")


def _expect_accept(name: str, fn, value) -> None:
    try:
        result = fn(value)
    except Exception as exc:
        raise AssertionError(f"{name} unexpectedly rejected the bad dtype") from exc
    print(f"{name}: accepted bad dtype -> {result}")


def main() -> None:
    int_array = jnp.array([1, 2, 3], dtype=jnp.int32)
    float_array = jnp.array([1.0, 2.0, 3.0])

    print("good input:")
    print("with_optional:", with_optional(int_array))
    print("with_union:   ", with_union(int_array))
    print("with_pipe:    ", with_pipe(int_array))

    print()
    print("bad input:")
    _expect_reject("with_optional", with_optional, float_array)
    _expect_reject("with_union", with_union, float_array)
    _expect_accept("with_pipe", with_pipe, float_array)

    print()
    print("BUG REPRODUCED: PEP 604 union accepts the bad dtype while Optional/Union reject it.")


if __name__ == "__main__":
    main()
