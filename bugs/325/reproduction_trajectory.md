# Reproduction Trajectory — Bug 325: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2146](https://github.com/pyro-ppl/numpyro/issues/2146)
- **Repository:** pyro-ppl/numpyro @ `78c366530db3c26075a63dba370ad002b17b006a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment with Python 3.12.
2. Installed the pinned runtime stack from `requirements.txt` and the local `codebase/` in editable mode.
3. Ran `bash run_repro.sh` with `JAX_PLATFORM_NAME=cpu` and `PYTHONWARNINGS=always`.
4. Observed repeated `DeprecationWarning`s in `repro_stderr.log` and successful sample values in `repro_stdout.log`.

## Observed behavior

- Running the local NumPyro checkout under JAX 0.9.1 with warnings enabled reproduces the reported issue: sampling `Dirichlet([1])` and `Beta(1, 1)` both emit `DeprecationWarning`s from `ml_dtypes/_finfo.py` about implicit array-to-dtype conversion, while still returning samples.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
