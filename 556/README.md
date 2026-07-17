# Bug 556 Reproduction

This folder contains a minimal reproduction for:

- Issue: https://github.com/huggingface/transformers/issues/46821
- Bug: `TimesFm 2.5` raises `AttributeError` when `window_size` is passed

The repro uses the local `codebase/` checkout directly and does not download the upstream checkpoint.

## Files

- `repro.py`: standalone Python repro
- `requirements.txt`: minimal dependency pin for the known incompatible hub version
- `setup_env.sh`: installs the repro dependencies
- `run_repro.sh`: runs the repro and writes logs plus `reproduction.json`
- `manifest.json`: machine-readable bundle metadata

## Reproduction summary

The bug is reproducible in the local checkout because `TimesFm2_5ModelForPrediction.forward()` calls the missing method `_timesfm_moving_average()`, while the class only defines `_timesfm2_5_moving_average()`.
