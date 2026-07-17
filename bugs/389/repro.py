#!/usr/bin/env python3
import os
import sys
import warnings

warnings.filterwarnings("ignore")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

try:
    import numpy as np
    import jax
    import jaxlib
    import jax.numpy as jnp
except ImportError as e:
    print(f"missing dep: {e}")
    sys.exit(2)

print("jax_version:", jax.__version__)
print("jaxlib_version:", jaxlib.__version__)
print("backend:", jax.default_backend())

nan = float("nan")
inf = float("inf")

x = jnp.asarray(
    np.asarray(
        [
            [nan, inf, -inf],
            [-0.35449573397636414, 0.04463260620832443, 0.11511584371328354],
        ],
        dtype=np.float32,
    )
)

y = jnp.asarray(
    np.asarray(
        [
            [-0.0, 0.0, 1.401298464324817e-45],
            [-1.0, 1.0, 9.999999974752427e-07],
        ],
        dtype=np.float32,
    )
)

out = np.asarray(jax.lax.mul(x, y))
expected = np.asarray(
    [
        [nan, nan, -inf],
        [0.35449573397636414, 0.04463260620832443, 1.1511584574463996e-07],
    ],
    dtype=np.float32,
)

print("jax:", out.tolist())
print("expected:", expected.tolist())
print("third_element_is_negative_inf:", np.isneginf(out[0, 2]).item())
print("third_element_is_nan:", np.isnan(out[0, 2]).item())
print("matches_expected:", bool(np.array_equal(out, expected, equal_nan=True)))

if np.isneginf(out[0, 2]):
    sys.exit(0)

print("BUG: -inf * positive subnormal returned", out[0, 2])
sys.exit(1)
