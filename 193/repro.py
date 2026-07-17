#!/usr/bin/env python3
"""Minimal reproduction for equinox issue 1172.

This script intentionally triggers the reported failure and treats the exact
`TypeError` as a reproduced bug.
"""

from __future__ import annotations

import json
import traceback

import equinox as eqx
import jax
import jax.numpy as jnp


class SomeNetwork(eqx.Module):
    layer: eqx.nn.Linear
    some_eqx_field_value: int = eqx.field(default=42, static=True)

    def __init__(self, key):
        self.layer = eqx.nn.Linear(3, 5, key=key)

    def __call__(self, x):
        return self.layer(x)


def main() -> int:
    key = jax.random.PRNGKey(0)
    critic = SomeNetwork(key)
    batch = jnp.zeros((1, 2, 3))

    def scan_fn(carry, x):
        # This is the reported trigger: vmapping over the carried Module.
        out = jax.vmap(carry)(x)
        return carry, out

    try:
        jax.lax.scan(scan_fn, critic, batch)
    except Exception as exc:  # noqa: BLE001
        message = str(exc)
        expected = 'can only concatenate str (not "_Sentinel") to str'
        reproduced = isinstance(exc, TypeError) and expected in message
        payload = {
            "reproduced": reproduced,
            "exception_type": type(exc).__name__,
            "exception_message": message,
            "jax_version": jax.__version__,
            "equinox_version": eqx.__version__,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        if reproduced:
            print("BUG REPRODUCED")
            return 0
        traceback.print_exc()
        return 1

    print("Unexpected success: bug not reproduced")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
