# Reproduction Trajectory — Bug 361: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47068](https://github.com/huggingface/transformers/issues/47068)
- **Repository:** huggingface/transformers @ `b70d02fc724d04c916832ca4ead03ff05e8fb1ee`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a fresh Python virtual environment and installed torch==2.7.1+cu128 plus transformers==4.57.2 from the cu128 PyTorch index.
2. Ran repro.py against the local Transformers source tree.
3. Observed the exact Python conditional path, but the isolated timing probe did not show a measurable host synchronization in this environment.

## Observed behavior

- The reported conditional is present in codebase/src/transformers/integrations/deepspeed.py:738-741.
- The local CUDA probe ran on torch 2.7.1+cu128 and printed branch_elapsed_ms=6.41, sync_elapsed_ms=6.49, then BUG_NOT_REPRODUCED.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug report depends on a distributed sequence-parallel all_gather path with CUDA tensors; the local single-process probe here does not reproduce the Nsight-observed host synchronization.
