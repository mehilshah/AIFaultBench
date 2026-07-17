# Reproduction Trajectory — Bug 353: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2613](https://github.com/huggingface/pytorch-image-models/issues/2613)
- **Repository:** huggingface/pytorch-image-models @ `ae4d1bbfefab7e4f2f49a744838a2d9c7713146d`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated virtualenv and installed a CPU-only torch/torchvision stack plus the minimal repo dependencies.
2. Ran run_repro.sh, which executed repro.py against the local codebase.
3. Observed that ROCm is not available in this environment, so the HIP invalid-argument failure from the issue cannot be exercised here.

## Observed behavior

- Captured runtime info in repro_stdout.log shows torch 2.9.0+cpu, cuda_available=false, and torch_hip=null.
- The same log shows Attention2d and MultiQueryAttention2d forward passes completed successfully on CPU with output shape [1, 128, 32, 48].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported bug requires an AMD ROCm runtime/GPU. This folder only has a CPU-only torch build and no ROCm device, so the HIP error cannot be reproduced locally.
