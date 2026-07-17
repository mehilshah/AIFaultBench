# Bug 191 Reproduction

This folder reproduces the Apex build failure reported in:
`https://github.com/NVIDIA/apex/issues/1823`

The failure happens when `pip install` builds Apex from source with PEP 517 build isolation. `setup.py` imports `torch` at module import time, but the isolated build environment only contains `setuptools` and `wheel`, so the build aborts with:

`ModuleNotFoundError: No module named 'torch'`

## Files

- `repro.py`: runs the failing install command and writes logs plus `reproduction.json`
- `requirements.txt`: minimal helper dependencies for the repro harness
- `setup_env.sh`: installs helper dependencies
- `run_repro.sh`: launcher used by automation

## Repro command

```bash
bash run_repro.sh
```

## Expected outcome

The command should fail during build isolation with `ModuleNotFoundError: No module named 'torch'`.
