# Bug 300 Reproduction

This bundle reproduces the `DiffusionPipeline.download()` offline-cache regression described in `bug_report.txt`.

## What it does

1. Downloads `google/ddpm-cifar10-32` once with a normal Hub connection.
2. Runs the same download again with `HF_HUB_OFFLINE=1`.
3. Confirms the second call fails after the first cache warmup.

## Files

- `repro.py` runs the two-phase reproduction.
- `requirements.txt` pins the bug-triggering Hub version and the minimal runtime dependencies.
- `setup_env.sh` creates `.venv` and installs dependencies.
- `run_repro.sh` runs the repro and captures stdout/stderr.

## Usage

```bash
bash setup_env.sh
bash run_repro.sh
cat reproduction.json
```
