# Reproduction Trajectory — Bug 293: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2174](https://github.com/pyro-ppl/numpyro/issues/2174)
- **Repository:** pyro-ppl/numpyro @ `0152376a197af90d0ce5198f8375e03069f29f48`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh virtual environment with Python 3.12 and installed the local NumPyro codebase editable together with `jax==0.10.0` and `jaxlib==0.10.0`.
2. Ran `repro.py`, which imports `jax` first to confirm the version and missing `xla_pmap_p` attribute.
3. Attempted to import `numpyro`, which immediately failed during module initialization in `numpyro.ops.provenance`.

## Observed behavior

- The repro environment installed JAX 0.10.0, and the pre-import probe printed `jax_version=0.10.0`.
- The same probe printed `has_xla_pmap_p=False`, matching the missing symbol reported in the bug.
- Importing `numpyro` failed with `ImportError: cannot import name 'xla_pmap_p' from 'jax.extend.core.primitives'` while executing `numpyro/ops/provenance.py`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
