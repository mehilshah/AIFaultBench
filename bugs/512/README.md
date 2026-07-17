# Bug 512

Repro bundle for the Lightning Fabric FSDP precision bug described in [`bug_report.txt`](./bug_report.txt).

## What this repro checks

The reported issue is that `FSDPPrecision("bf16-mixed").module_init_context()` initializes module parameters in `torch.bfloat16` instead of keeping them in full precision (`torch.float32`).

This bundle reproduces that directly in `repro.py` without requiring a CUDA device or distributed launch.

## Files

- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`manifest.json`](./manifest.json)

## How to run

1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro is expected to fail with an `AssertionError` showing that the initialized dtype is `torch.bfloat16`.
