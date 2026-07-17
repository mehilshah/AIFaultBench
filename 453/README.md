# Bug 453

This folder contains a self-contained reproduction bundle for:
`https://github.com/deepspeedai/DeepSpeed/issues/7811`

Included source inputs:
- `bug_report.txt`
- `codebase/` checked out at `5b2ccad96a2e8f0567f08714a07aa0baca11c7ef`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `ds_config_zero3_stress.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run order:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Notes:
- The repro uses `torchrun --nproc_per_node=2`.
- The bug path is DeepSpeed ZeRO-3 `GatheredParameters(..., modifier_rank=None)` with in-place slice touches.
- This host needed a Blackwell-capable PyTorch wheel (`torch==2.7.0+cu128`) to get past CUDA initialization.
