# Reproduction Trajectory — Bug 564: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2022](https://github.com/pyro-ppl/numpyro/issues/2022)
- **Repository:** pyro-ppl/numpyro @ `7c7a7e9a1814adc0ad5e919427723dbab3ee9410`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an `nnx.Module` whose child layers are stored in a Python list.
2. Call `numpyro.contrib.module.random_nnx_module("nn", module, prior)` inside a seeded NumPyro model.
3. The recursive parameter walk reaches an integer list index and fails when `_update_params` tries to build the dotted path name.

## Observed behavior

- Running `bash run_repro.sh` raises `TypeError: sequence item 1: expected str instance, int found` from `codebase/numpyro/contrib/module.py:234` inside `_update_params` while `random_nnx_module` recursively processes list-backed NNX layers.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
