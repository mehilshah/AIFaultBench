# Reproduction Bundle

Bug: `BERT/PyTorch` `gelu()` passes `approximate=True` to `torch.nn.functional.gelu`, which raises a `TypeError` on current PyTorch releases.

## Contents

- `repro.py`: loads the local BERT `modeling.py` and calls `gelu`
- `file_utils.py`: minimal shim so the BERT module imports cleanly
- `requirements.txt`: runtime dependency list
- `setup_env.sh`: installs dependencies
- `run_repro.sh`: executes the repro

## Repro

1. `bash setup_env.sh`
2. `bash run_repro.sh`

Expected result: `TypeError: gelu(): argument 'approximate' must be str, not bool`
