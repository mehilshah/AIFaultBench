# Bug 513 Reproduction Bundle

This folder contains a self-contained repro for Hugging Face Accelerate issue 1183.

## What the repro checks

The script launches 4 CPU distributed workers and exercises:

- `Accelerator.main_process_first()`
- `Accelerator.local_main_process_first()`

Rank 0 intentionally sleeps inside the guarded block. If the context managers work,
other ranks still wait and rank 0 prints first. In this snapshot, the non-main ranks
enter the block early, so the recorded order starts with rank 2 instead of rank 0.

## Files

- `repro.py`: distributed repro and assertion
- `requirements.txt`: runtime dependencies for the repro venv
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro in the prepared environment
- `manifest.json`: benchmark metadata
- `reproduction.json`: machine-readable result
- `repro_stdout.log` / `repro_stderr.log`: captured run output

## Run

1. `bash setup_env.sh`
2. `bash run_repro.sh`

Expected result in this snapshot: the script raises `RuntimeError` because the
first recorded `main` event is not rank 0.
