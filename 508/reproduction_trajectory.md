# Reproduction Trajectory — Bug 508: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2053](https://github.com/pyro-ppl/numpyro/issues/2053)
- **Repository:** pyro-ppl/numpyro @ `0d4f40c5a25633591388f12372cdb31f9dff0f29`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh venv with python3 -m venv .venv
2. Install requirements from requirements.txt and install the local codebase with pip install --no-deps -e codebase
3. Run python repro.py to import numpyro

## Observed behavior

- In an isolated Python 3.12 virtual environment, installing the local NumPyro snapshot with its runtime dependencies but without typing_extensions and then running import numpyro fails with ModuleNotFoundError: No module named 'typing_extensions'. The traceback enters numpyro/_typing.py from numpyro/distributions/conjugate.py during the top-level import.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
