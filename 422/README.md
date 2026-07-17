# Bug 422

This folder contains a self-contained reproduction bundle for Lightning issue 21635.

## What reproduces

`lightning/fabric/strategies/deepspeed.py` validates checkpoint paths with `pathlib.Path`.  
For URI-like paths such as `s3://...`, `Path(...)` normalizes the string to `s3:/...`, and the
validation helper raises `FileNotFoundError` on the mangled local path.

## Repro status

Reproduced in this folder with the checked-out Lightning commit from `codebase/`.

## Files

- `repro.py`: minimal harness that loads the helper functions from the checked-out source file and exercises the failing URI case
- `run_repro.sh`: executes the harness
- `setup_env.sh`: environment bootstrap stub
- `requirements.txt`: no third-party dependencies needed for the harness
- `repro_stdout.log`, `repro_stderr.log`: captured run output
- `reproduction.json`: schema-constrained result record

## Reproduction command

`bash run_repro.sh`
