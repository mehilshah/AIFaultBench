# Bug 526 Reproduction

This folder reproduces the `CrossQLoss` constructor failure reported in
https://github.com/pytorch/rl/issues/3309.

## What fails

Passing a numeric `target_entropy` to `CrossQLoss` raises:

`UnboundLocalError: cannot access local variable 'device' where it is not associated with a value`

The failure happens in:

`codebase/torchrl/objectives/crossq.py`

when the constructor reaches:

`torch.tensor(target_entropy, device=device)`

but `device` is only defined inside the `"auto"` branch.

## Reproduction

1. Run `./run_repro.sh`
2. Inspect `repro_stdout.log` and `repro_stderr.log`

## Files

- `repro.py`: minimal failing constructor call
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `reproduction.json`: machine-readable reproduction result
