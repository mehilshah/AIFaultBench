# Reproduction Trajectory — Bug 459: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2064](https://github.com/pyro-ppl/numpyro/issues/2064)
- **Repository:** pyro-ppl/numpyro @ `ddbd0b876d3cf07d457683d520f00c85f0cc0bb8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install the pinned dependencies from requirements.txt.
2. Run bash run_repro.sh from the standardized bug folder.
3. Observe the TypeError in repro_stderr.log and the REPRODUCED marker in repro_stdout.log.

## Observed behavior

- On the checked-out numpyro commit ddbd0b876d3cf07d457683d520f00c85f0cc0bb8, calling get_model_relations() on a guide with numpyro.param('p', lambda _: 1.0) raises TypeError: Value <function guide.<locals>.<lambda> ...> is not a valid JAX type.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
