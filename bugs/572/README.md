# Bug 572 Reproduction Bundle

This folder contains a self-contained repro bundle for:

- Issue: https://github.com/huggingface/accelerate/issues/1004
- Library: `accelerate`
- Reported version: `0.15.0`

## Contents

- `bug_report.txt`: original issue report
- `codebase/`: local source snapshot used to infer the repro
- `repro.py`: minimal script matching the reported DeepSpeed generation loop
- `requirements.txt`: Python dependencies for the repro environment
- `setup_env.sh`: creates a virtualenv and installs the deps
- `run_repro.sh`: launcher with a GPU-count preflight check
- `reproduction.json`: machine-readable outcome
- `repro_stdout.log` / `repro_stderr.log`: captured run output

## Result

The bug is not reproducible in this folder as-is because the reported failure needs multiple GPUs and this machine only exposes one visible CUDA device.

## How to run

```bash
./setup_env.sh
./run_repro.sh
```

On a machine with 2+ GPUs and a compatible DeepSpeed installation, `repro.py` runs the same `model.generate(..., max_new_tokens=5)` pattern from the issue report.
