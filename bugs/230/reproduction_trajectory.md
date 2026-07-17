# Reproduction Trajectory — Bug 230: optuna

- **Bug report:** [https://github.com/optuna/optuna/issues/5780](https://github.com/optuna/optuna/issues/5780)
- **Repository:** optuna/optuna @ `7128a94`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv and installed the minimal runtime dependencies from requirements.txt.
2. Ran `bash run_repro.sh` with PYTHONPATH pointing at the local codebase.
3. Observed three completed trials instead of the full 2x2 grid; stdout and stderr were saved to repro_stdout.log and repro_stderr.log.

## Observed behavior

- Running the BruteForceSampler MRE with n_jobs=2 produced only 3 trials and missed the parameter combination {'x': 1, 'y': 1}; the repro script raised AssertionError: Incomplete brute-force coverage.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
