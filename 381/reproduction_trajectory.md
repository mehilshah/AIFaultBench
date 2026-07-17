# Reproduction Trajectory — Bug 381: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47935](https://github.com/vllm-project/vllm/issues/47935)
- **Repository:** vllm-project/vllm @ `4aceabf8c1a40f8d576ba9b83e4b9a8854eda2d5`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspect the issue source and the relevant FlashMLA code path.
2. Attempted to import torch; the local environment failed before FlashMLA could load.

## Observed behavior

- The current source already pads C128A top-k width to 128 in vllm/models/deepseek_v4/sparse_mla.py.
- FlashMLA sparse support is gated to Hopper/Blackwell in vllm/v1/attention/ops/flashmla.py.
- torch import failed: ImportError: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommResume

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

torch import failed: ImportError: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so: undefined symbol: ncclCommResume
