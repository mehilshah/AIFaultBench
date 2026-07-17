# Bug 444

Reproduction bundle for numpyro issue 2071, "Parallel Predictive with new-style prng keys".

The bug reproduces on the local `codebase/` checkout at commit `68d86dc0535c5488f497790af2305d19d74d924a` with:

- `jax==0.7.1`
- `jaxlib==0.7.1`
- `numpyro==0.19.0` from the local checkout

## What fails

`Predictive(..., parallel=True)` works with legacy `jax.random.PRNGKey(0)` but raises:

`ValueError: Cannot convert_element_type from int32 to key<fry>`

when called with the new typed key `jax.random.key(0)`.

The failing path is in `numpyro/util.py:soft_vmap`, which pads the RNG-key pytree and hits JAX's typed-key conversion error.

## How to run

1. `bash setup_env.sh`
2. `bash run_repro.sh`

`run_repro.sh` is expected to fail for the typed-key case and print the traceback.

