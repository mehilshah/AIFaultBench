#!/usr/bin/env python3
"""Minimal reproduction for numpyro issue 2055 / flax 0.11.0 incompatibility."""

from __future__ import annotations

from jax import random
import numpyro
from numpyro.contrib.module import nnx_module
import numpyro.distributions as dist


def run_case(batchnorm: bool) -> None:
    from flax import nnx

    class Net(nnx.Module):
        def __init__(self, *, rngs):
            if batchnorm:
                self.bn = nnx.BatchNorm(3, rngs=rngs)
            # The reported regression is that this constructor now looks for a
            # "dropout" stream even when the caller only provided params.
            self.dropout = nnx.Dropout(rate=0.5, deterministic=True, rngs=rngs)

        def __call__(self, x, *, rngs=None):
            x = self.dropout(x, deterministic=True)
            if batchnorm:
                x = self.bn(x)
            return x

    rng_key = random.PRNGKey(0)

    # This mirrors the reported test setup; the failure happens before the
    # NumPyro model is entered.
    net_module = Net(rngs=nnx.Rngs(params=rng_key))

    def model():
        nn = nnx_module("nn", net_module)
        x = numpyro.sample("x", dist.Normal(0, 1).expand([4, 3]).to_event(2))
        y = nn(x)
        numpyro.deterministic("y", y)

    _ = model


def main() -> int:
    failures = []
    for batchnorm in (False, True):
        label = "batchnorm" if batchnorm else "no_batchnorm"
        print(f"case={label}")
        try:
            run_case(batchnorm)
            print("  ok")
        except Exception as exc:  # noqa: BLE001
            print(f"  failed: {type(exc).__name__}: {exc}")
            failures.append((label, type(exc).__name__, str(exc)))

    if failures:
        print("summary: reproduces the reported flax 0.11.0 KeyError")
        for label, exc_type, message in failures:
            print(f"  {label}: {exc_type}: {message}")
        return 1

    print("summary: no failure observed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
