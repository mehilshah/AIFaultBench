# Reproduction Trajectory — Bug 187: marimo

- **Bug report:** [https://github.com/marimo-team/marimo/issues/7969](https://github.com/marimo-team/marimo/issues/7969)
- **Repository:** marimo-team/marimo @ `62cd22c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a notebook-style runtime context with tests.conftest.MockedKernel.
2. Call await app.embed(defs={'arr': np.ones(1)}) once to seed the cache.
3. Call await app.embed(defs={'arr': np.zeros(2)}) and observe the ValueError.

## Observed behavior

- Running ./repro.py in a notebook-style kernel context triggers a ValueError on the second embed call. The exception originates in marimo/_runtime/app/kernel_runner.py:119, where are_outputs_cached() does `defs == self._previously_seen_defs`; comparing numpy arrays with different shapes produces `ValueError: The truth value of an array with more than one element is ambiguous`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
