# Reproduction Trajectory — Bug 245: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2117](https://github.com/pyro-ppl/numpyro/issues/2117)
- **Repository:** pyro-ppl/numpyro @ `6a1af1f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh virtual environment in this folder.
2. Install jax==0.8.2 and jaxlib==0.8.2 into the virtual environment.
3. Run repro.py with PYTHONWARNINGS=error::DeprecationWarning and the local codebase on PYTHONPATH.
4. Observe the traceback from jax.interpreters.pxla.xla_pmap_p during import of numpyro.

## Observed behavior

- With jax==0.8.2 installed, importing numpyro from the local codebase fails under DeprecationWarning-as-error at codebase/numpyro/ops/provenance.py line 1: from jax.interpreters.pxla import xla_pmap_p. JAX raises DeprecationWarning: jax.interpreters.pxla.xla_pmap_p is deprecated as of JAX v0.8.2.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
