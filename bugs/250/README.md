# TorchRL replay-buffer pinning repro

This bundle reproduces the TorchRL issue where `TensorDictReplayBuffer(pin_memory=True)` does not pin
samples after a custom transform creates a new `TensorDict` without an explicit device.

## Reproduction

```bash
bash run_repro.sh
```

Expected output in this environment:

```text
sample.device=None
observation.device=cpu
observation.is_pinned=False
```

The failure matches the bug report: the transform returns a CPU tensor, but the returned `TensorDict`
has `device=None`, so the replay-buffer pinning helper skips it.

## Environment

- Python 3.12
- `torch==2.4.0+cpu`
- `tensordict==0.5.0`

## Files

- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`

