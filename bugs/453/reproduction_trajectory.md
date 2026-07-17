# Reproduction Trajectory — Bug 453: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7811](https://github.com/deepspeedai/DeepSpeed/issues/7811)
- **Repository:** microsoft/DeepSpeed @ `5b2ccad96a2e8f0567f08714a07aa0baca11c7ef`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a venv and installed `torch==2.7.0+cu128` plus the editable DeepSpeed checkout from `codebase/`.
2. Verified that single-rank execution on the available GPU completes DeepSpeed initialization and the repro loop without the issue.
3. Attempted the reported 2-rank ZeRO-3 launch, but the host exposes only one visible CUDA device, so NCCL aborts with duplicate-GPU detection before the reported `GatheredParameters` exit path is reached.

## Observed behavior

- Single-rank probe on this host reached DeepSpeed ZeRO-3 initialization and completed the gather loop without the reported assert: `[rank0] step=25 ok`, `[rank0] step=50 ok`, `RESULT hit=False exc=None`.
- Two-rank probe failed before the bug path with NCCL duplicate-device invalid usage: `Duplicate GPU detected : rank 0 and rank 1 both on CUDA device ac000` and `DistBackendError` during `deepspeed.initialize()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
VOCAB=4096 D_MODEL=512 ITERS=50 NPROC_PER_NODE=2 bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This machine has only one visible CUDA device, so the reported 2-rank NCCL topology cannot be reproduced here. The 2-rank attempt fails during distributed initialization with duplicate-GPU NCCL invalid usage, before the DeepSpeed `free_param()` assert can occur.
