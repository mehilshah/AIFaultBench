# Reproduction Trajectory — Bug 574: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47037](https://github.com/vllm-project/vllm/issues/47037)
- **Repository:** vllm-project/vllm @ `59575da46df964e6161fb0e1a77fa76ea9ce3106`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Built a self-contained repro bundle from the bug report and local `codebase/` snapshot.
2. Ran `bash run_repro.sh` and captured the output in `repro_stdout.log` and `repro_stderr.log`.
3. Confirmed that the local runtime cannot import torch, so the Hopper/FlashInfer FP8 reproduction path cannot be exercised here.

## Observed behavior

- Running `bash run_repro.sh` exited in preflight before any vLLM server or LM-Eval process was started.
- The captured stdout says `torch import failed: ImportError: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommResume`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This workspace has a broken local torch installation (`libtorch_cuda.so` is missing `ncclCommResume`), so the CUDA/vLLM stack needed by the report cannot start here.
