# Reproduction Trajectory — Bug 248: Eel

- **Bug report:** [https://github.com/python-eel/Eel/issues/748](https://github.com/python-eel/Eel/issues/748)
- **Repository:** python-eel/Eel @ `ff1fa20`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtual environment.
2. Install the local `codebase/` package with pip.
3. Run `import eel` via `repro.py`.
4. Observe the missing `typing_extensions` runtime dependency error.

## Observed behavior

- In a fresh virtualenv, `pip install ./codebase` succeeds and `python repro.py` fails at `import eel` with `ModuleNotFoundError: No module named 'typing_extensions'` from `eel/__init__.py:6`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
