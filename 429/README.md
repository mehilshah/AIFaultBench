# Bug 429 Repro

Reported issue: `https://github.com/pytorch/rl/issues/3549`

The reported crash happens when `SyncDataCollector` moves a `GymEnv("HalfCheetah-v4")`
environment to `mps` and the environment specs include float64 tensors.

Files in this bundle:
- `repro.py` - minimal Python repro
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - creates a local virtual environment and installs deps
- `run_repro.sh` - entry point for the repro

Current host note:
- this folder was verified on a Linux host without MPS, so the repro is blocked here
  before the collector can be constructed.
