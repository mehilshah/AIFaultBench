# Reproduction Trajectory — Bug 577: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2019](https://github.com/pyro-ppl/numpyro/issues/2019)
- **Repository:** pyro-ppl/numpyro @ `ff6f5675249d6192e1f8613f8b073f70c8898ba2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtual environment and install the pinned dependencies from requirements.txt.
2. Install the local NumPyro tree in editable mode.
3. Run `bash run_repro.sh` to execute repro.py and capture the traceback.

## Observed behavior

- Running `bash run_repro.sh` under jax==0.6.0, jaxlib==0.6.0, and dm-haiku==0.0.13 fails during `import haiku as hk` with `AttributeError: jax.core.JaxprEqn was removed in JAX v0.6.0`. The traceback shows the failure originates in `haiku/_src/jaxpr_info.py` while importing `haiku.experimental.jaxpr_info`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
