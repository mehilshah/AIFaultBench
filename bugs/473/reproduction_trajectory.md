# Reproduction Trajectory — Bug 473: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2055](https://github.com/pyro-ppl/numpyro/issues/2055)
- **Repository:** pyro-ppl/numpyro @ `0d4f40c5a25633591388f12372cdb31f9dff0f29`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv with `bash setup_env.sh`.
2. Installed `numpyro` from the local codebase plus `flax==0.11.0`, `jax==0.6.2`, and `jaxlib==0.6.2`.
3. Executed `bash run_repro.sh` and observed the reported NNX dropout `KeyError` in both smoke-test variants.

## Observed behavior

- bash run_repro.sh exited with status 1.
- repro_stdout.log shows both `no_batchnorm` and `batchnorm` cases failing with `KeyError: "No RngStream named 'dropout' found in Rngs."`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
