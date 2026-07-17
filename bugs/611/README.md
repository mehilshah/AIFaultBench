# Bug 611 Reproduction

This folder reproduces the `accelerate` issue where `gather_for_metrics` keeps using a stale `GradientState` after an evaluation loop is run in the middle of training.

## What the repro shows

Running evaluation on a prepared dataloader updates the shared `GradientState` to `end_of_dataloader=True`. When training resumes on a previously created train dataloader iterator, `gather_for_metrics` incorrectly truncates a non-final train batch.

## Files

- `bug_report.txt`: original issue summary
- `codebase/`: local `accelerate` source snapshot
- `repro.py`: minimal failing script
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates an isolated environment and installs dependencies
- `run_repro.sh`: runs the repro script
- `manifest.json`: metadata for this standardized bug folder
- `reproduction.json`: machine-readable result
- `repro_stdout.log`, `repro_stderr.log`: captured run output

## Reproduction

```bash
./run_repro.sh
```
