# Reproduction Trajectory — Bug 591: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/2886](https://github.com/pyro-ppl/pyro/issues/2886)
- **Repository:** pyro-ppl/pyro @ `ced727e579c50654bdf264604652d93fe663c0d5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.9 virtualenv.
2. Install the pinned dependencies from requirements.txt.
3. Run PYTHONPATH=codebase .venv/bin/python repro.py.

## Observed behavior

- In a Python 3.9 virtualenv with torch 1.9.0+cpu and the local Pyro 1.6.0 checkout, running the report's sequential-enumeration snippet prints the model shapes and then fails with RuntimeError: unsupported input to tensordot, got dims=0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
