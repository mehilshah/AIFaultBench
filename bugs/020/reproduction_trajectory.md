# Reproduction Trajectory — Bug 020: models

- **Bug report:** [https://github.com/tensorflow/models/issues/10986](https://github.com/tensorflow/models/issues/10986)
- **Repository:** tensorflow/models @ `631e763896a7cc4be6edf20c659938e02715fee8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the bug folder.
2. The script starts a Python 3.8 container, mounts the folder, and executes `repro.py`.
3. The script reads `codebase/official/core/base_trainer.py` and exercises the same `dict | dict` merge path reported in the bug.
4. Python 3.8 fails with the reported TypeError.

## Observed behavior

- docker run --rm python:3.8-slim python --version reports Python 3.8.20.
- codebase/official/core/base_trainer.py:442 contains `return passthrough_logs | logs`.
- Running the bundled repro under Python 3.8 raises `TypeError: unsupported operand type(s) for |: 'dict' and 'dict'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
