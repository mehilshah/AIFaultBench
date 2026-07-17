# Bug 324 Reproduction

This folder contains a self-contained repro for TorchRL issue 3840.

## What it tests

`MultiSyncCollector` with 16 workers and a 1.1 second environment step delay.

The bug report says:

- `preemptive_threshold=1.0` takes about 16 seconds
- `preemptive_threshold=0.99` takes about 1 second

That difference points to extra `queue_out.get(timeout=_TIMEOUT)` calls after all worker results are already available.

## Files

- `repro.py`: minimal reproduction script
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates the virtualenv and installs dependencies
- `run_repro.sh`: sets up the env and runs the repro
- `manifest.json`: metadata for this standardized folder

## Run

```bash
bash run_repro.sh
```

Expected output:

- `preemptive_threshold=1.0` around 16 seconds
- `preemptive_threshold=0.99` around 1 second
- `bug_reproduced=yes`
