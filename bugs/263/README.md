# Bug 263 Reproduction

This folder contains a self-contained reproduction for Tianshou issue 1272.

## What fails

`ShmemVectorEnv` with `gymnasium.wrappers.FrameStack` returns stale stacked observations after `step()`.

The same environment logic works with `DummyVectorEnv`, but the shared-memory worker path in `ShmemVectorEnv` leaves the frame buffer frozen at the reset value.

## Files

- `bug_report.txt`: original bug report
- `codebase/`: local source snapshot used to infer the package and dependency context
- `repro.py`: minimal reproduction script
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `manifest.json`: metadata for the standardized bundle
- `reproduction.json`: machine-readable reproduction result

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

Or, inside Docker:

```bash
```

## Expected result

The repro prints that `DummyVectorEnv` updates the stacked frames, while `ShmemVectorEnv` keeps returning `[[[0], [0], [0]]]` after each step.
