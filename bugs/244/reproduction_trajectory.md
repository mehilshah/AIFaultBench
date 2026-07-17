# Reproduction Trajectory — Bug 244: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2053](https://github.com/pyro-ppl/numpyro/issues/2053)
- **Repository:** pyro-ppl/numpyro @ `0d4f40c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh virtual environment.
2. Install the runtime dependencies from requirements.txt and the local codebase/ package.
3. Confirm typing_extensions is not installed in that environment.
4. Run `import numpyro` and observe the import-time ModuleNotFoundError.

## Observed behavior

- Fresh venv run installed numpyro without typing_extensions present (`typing_extensions_installed=False`). Importing numpyro failed in numpyro/_typing.py with `ModuleNotFoundError: No module named 'typing_extensions'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
