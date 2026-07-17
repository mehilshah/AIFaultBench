# Reproduction Trajectory — Bug 326: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3314](https://github.com/pyro-ppl/pyro/issues/3314)
- **Repository:** pyro-ppl/pyro @ `1a11185ce54a2391348bec5919f3330d957d2f98`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.12 virtual environment and installed `mypy==1.8.0`.
2. Installed `codebase/` in editable mode with dependencies disabled.
3. Ran `bash run_repro.sh`, which executes `repro.py` and checks mypy against an external file importing Pyro modules.

## Observed behavior

- Editable-installing the local codebase leaves `py.typed` absent in `codebase/pyro/`, and mypy reports 5 `import-not-found` errors for `pyro`, `pyro.distributions`, `pyro.infer`, `pyro.infer.autoguide`, and `pyro.optim`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
