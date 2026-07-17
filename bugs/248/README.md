# Bug 248

This folder contains a self-contained reproduction of the Eel 0.18.0 import
failure caused by the missing `typing_extensions` runtime dependency.

Repro flow:
1. Create a fresh virtual environment.
2. `pip install` the local `codebase/` package.
3. Run `import eel`.
4. Observe `ModuleNotFoundError: No module named 'typing_extensions'`.

Files:
- `bug_report.txt`: source report
- `codebase/`: local package snapshot
- `repro.py`: import check that surfaces the exception
- `requirements.txt`: intentionally empty; do not preinstall `typing_extensions`
- `setup_env.sh`: creates a clean virtual environment
- `run_repro.sh`: installs the package and runs the repro
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log` / `repro_stderr.log`: captured command output

The package metadata in `codebase/setup.py` does not list `typing_extensions`
in `install_requires`, while `eel/__init__.py` imports it at module import time.
