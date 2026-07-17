# Reproduction Trajectory — Bug 454: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/47303](https://github.com/vllm-project/vllm/issues/47303)
- **Repository:** vllm-project/vllm @ `63fcce4de1563309ea5195ba98d0a2e1ba4f5831`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read bug_report.txt and the checked-out vLLM source tree.
2. Checked GPU details with nvidia-smi.
3. Probed the local Python environment for torch and triton_kernels availability.

## Observed behavior

- The local GPU is NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition with compute capability 12.0, while the issue is described as Hopper-only (sm90).
- The base Python environment cannot import torch: /users/grad/mehil/.local/lib/python3.12/site-packages/torch/lib/libtorch_cuda.so fails with undefined symbol ncclCommResume.
- triton_kernels is not installed in this workspace.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This machine is not a Hopper (sm90) system, and the required Python environment is incomplete/broken for the Triton kernel path, so the reported NaN corruption cannot be exercised here.
