#!/usr/bin/env python3
import os

# Force CPU execution so the repro stays self-contained.
os.environ["JAX_PLATFORMS"] = "cpu"

import jax
import jax.numpy as jnp
import jax.experimental.pallas as pl


def copy_kernel(x_ref, out_ref):
    out_ref[...] = x_ref[...]


def main():
    print(f"jax={jax.__version__}")
    print(f"jaxlib={__import__('jaxlib').__version__}")
    print(f"backend={jax.default_backend()}")

    x = jnp.ones((1, 512), dtype=jnp.bfloat16)
    out = pl.pallas_call(
        copy_kernel,
        out_shape=jax.ShapeDtypeStruct((1, 512), jnp.bfloat16),
        grid=(1, 4),
        in_specs=[
            pl.BlockSpec(
                index_map=lambda i, j: (i, j * 128),
                block_shape=(1, 128),
            )
        ],
        out_specs=pl.BlockSpec(
            index_map=lambda i, j: (i, j * 128),
            block_shape=(1, 128),
        ),
        interpret=True,
    )(x)

    nan_mask = jnp.isnan(out)
    nan_count = int(nan_mask.sum())
    print(f"nan_count={nan_count}")

    block_statuses = []
    for block_idx in range(4):
        block = out[0, block_idx * 128 : (block_idx + 1) * 128]
        is_nan = bool(jnp.isnan(block).any())
        is_all_ones = bool((block == 1.0).all()) if not is_nan else False
        if is_nan:
            status = "nan"
        elif is_all_ones:
            status = "ok"
        else:
            status = "wrong"
        block_statuses.append(status)
        print(f"block_{block_idx}={status}")

    expected = ["ok", "nan", "nan", "ok"]
    if block_statuses != expected:
        raise SystemExit(
            f"unexpected output pattern: got {block_statuses}, expected {expected}"
        )

    print("reproducible=True")


if __name__ == "__main__":
    main()
