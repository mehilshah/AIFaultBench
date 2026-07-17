# Reproduction Trajectory — Bug 633: jax

- **Bug report:** [https://github.com/jax-ml/jax/issues/37921](https://github.com/jax-ml/jax/issues/37921)
- **Repository:** jax-ml/jax @ `f4f5503bfa0db535cb505c2653b9f087a2dabc9d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed jaxlib 0.10.1 plus numpy/scipy/ml_dtypes/opt_einsum.
2. Ran repro.py with PYTHONPATH pointing at the local codebase.
3. Observed that numpy.searchsorted returned int64 and jnp.searchsorted returned int32 in both x32 and x64 modes.

## Observed behavior

- In the local source tree, jnp.searchsorted returns int32 for the sample inputs in both jax_enable_x64=False and jax_enable_x64=True, while numpy.searchsorted returns int64. The captured output in repro_stdout.log shows identical values with the wrong JAX dtype.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
