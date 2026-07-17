# Bug 605 Repro

This folder reproduces SDV issue 2703 from the bundled `bug_report.txt`.

Observed behavior in this checkout:
- `SingleTableDayZSynthesizer.validate_parameters(...)` accepts multi-table metadata when `relationships` is absent.
- `MultiTableDayZSynthesizer.validate_parameters(...)` raises `AttributeError` when a relationship entry is not a dictionary.
- `min_cardinality=0` is accepted.

Files:
- `repro.py`: standalone reproduction script.
- `requirements.txt`: installs the local codebase in editable mode.
- `setup_env.sh`: creates a venv and installs dependencies.
- `run_repro.sh`: runs the repro script.

Run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repo keeps the source bundle reusable by leaving `bug_report.txt` and `codebase/` untouched.
