# Bug 563 Reproduction

This folder contains a self-contained reproduction for the `check_env_specs()` key-mismatch bug reported in pytorch/rl issue 3260.

## What fails

`check_env_specs()` raises an `AssertionError` when the environment has a `state_spec` entry that is not part of the observation and the step output carries that state under `next`.

The minimal reproducer in `repro.py` mirrors the issue shape:

- nested `agents` composite specs
- `randomStates` in `state_spec` but not `observation_spec`
- `check_env_specs()` compares a fake rollout against a real rollout and sees extra `next` keys in the real data

## Files

- `repro.py`: minimal environment and failing call
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates a venv and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: schema-constrained reproduction result

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail with an `AssertionError` from `check_env_specs()`.
