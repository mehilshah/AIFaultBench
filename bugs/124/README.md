# Stable-Baselines3 repro bundle

This folder reproduces the nested `Sequence` space bug reported in
https://github.com/DLR-RM/stable-baselines3/issues/2172.

## Files

- `bug_report.txt`: original issue report
- `codebase/`: checked-in source snapshot used for the repro
- `repro.py`: minimal script that exercises `check_env` on nested `Sequence` spaces
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a venv and installs dependencies
- `run_repro.sh`: runs the repro and stores stdout/stderr logs

## Usage

```bash
bash setup_env.sh
bash run_repro.sh
```

The run should raise assertions for nested `Sequence` spaces inside `Dict`,
`Tuple`, and `OneOf` containers.
