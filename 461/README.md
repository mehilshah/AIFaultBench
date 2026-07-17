# Bug 461

This folder contains a minimal reproduction for SDV issue 2799.

Observed behavior:
- `Metadata().detect_from_dataframes(..., foreign_key_inference_algorithm='column_name_match')`
  does not create a relationship for a semantic foreign key column such as `email`.

Files:
- `repro.py`: self-contained reproducer that loads only the metadata modules needed for the bug.
- `requirements.txt`: Python dependencies used by the repro environment.
- `setup_env.sh`: creates `.venv` and installs the repro dependencies.
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`.

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail with an assertion because the detected metadata contains
`relationships: []` instead of the expected foreign-key relationship.
