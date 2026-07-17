# Bug 252 Reproduction Bundle

This folder reproduces the `PrioritizedSampler.loads()` failure reported in TorchRL issue [#3056](https://github.com/pytorch/rl/issues/3056).

## Contents
- `bug_report.txt`: source issue description
- `codebase/`: local TorchRL source snapshot used for inspection
- `repro.py`: minimal repro with a pure-Python segment-tree shim
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates a clean venv and installs dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail with:

- `AttributeError: 'NoneType' object has no attribute 'copy_'`

`run_repro.sh` stores the command output in:
- `repro_stdout.log`
- `repro_stderr.log`

## What is being exercised

The issue is in `torchrl/data/replay_buffers/samplers.py` inside `PrioritizedSampler.loads()`. A fresh sampler starts with `_max_priority == (None, None)`, and the load path attempts to run `copy_()` on those `None` values before the stored metadata is applied.
