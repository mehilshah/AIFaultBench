# Bug 491 Repro Bundle

This folder reproduces the `Composite.encode()` batch size bug reported in
https://github.com/pytorch/rl/issues/3409.

## What it shows

The repro creates a `Composite` spec with `shape=(2,)`, samples from it, and
passes a plain `dict` into `encode()`.

Observed output:

```text
torch.Size([2])
torch.Size([2])
torch.Size([])
```

That last line is the bug: the encoded `TensorDict` gets an empty `batch_size`
instead of `torch.Size([2])`.

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr
- `manifest.json`: bundle metadata

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
