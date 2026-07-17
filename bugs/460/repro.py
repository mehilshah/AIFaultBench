#!/usr/bin/env python3
"""Minimal reproduction for Pyro issue 3181.

This script runs the exact comparison from the issue report and prints the
observed shapes. It exits successfully when the mismatch is not present.
"""

from __future__ import annotations

from torch.distributions import LKJCholesky, TransformedDistribution, biject_to

from pyro import __version__ as pyro_version
from pyro.distributions import LKJCholesky as PyroLKJCholesky


def describe(label: str, dist) -> None:
    print(f"{label}.batch_shape = {dist.batch_shape}")
    print(f"{label}.event_shape = {dist.event_shape}")


def main() -> int:
    print(f"pyro_version = {pyro_version}")

    torch_lkj = LKJCholesky(2, 0.5)
    torch_inv = biject_to(torch_lkj.support).inv
    torch_transformed = TransformedDistribution(torch_lkj, torch_inv)
    describe("torch_transformed", torch_transformed)

    pyro_lkj = PyroLKJCholesky(2, 0.5)
    pyro_inv = biject_to(pyro_lkj.support).inv
    pyro_transformed = TransformedDistribution(pyro_lkj, pyro_inv)
    describe("pyro_transformed", pyro_transformed)

    if pyro_transformed.event_shape != torch_transformed.event_shape:
        raise AssertionError(
            "event_shape mismatch: "
            f"pyro={pyro_transformed.event_shape}, "
            f"torch={torch_transformed.event_shape}"
        )

    print("event_shape comparison passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
