# Reproduction Bundle

This bundle reproduces the xformers bug where `BlockDiagonalCausalMask.to()` returns a `BlockDiagonalMask` instead of preserving the causal subclass.

## What it does

`repro.py` creates a `BlockDiagonalCausalMask` from sequence lengths `[2, 2]`, moves it to `cpu`, and checks:

1. The returned object type.
2. The materialized mask before and after `.to()`.

The bug is reproduced when the moved mask is no longer a `BlockDiagonalCausalMask` and its materialization becomes non-causal.

## Run

```bash
bash run_repro.sh
```

## Files

- `repro.py`: minimal failing script
- `requirements.txt`: dependency list
- `setup_env.sh`: local virtualenv setup
- `run_repro.sh`: executes the repro
- `manifest.json`: bundle metadata
