# Reproduction Trajectory — Bug 338: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2616](https://github.com/huggingface/pytorch-image-models/issues/2616)
- **Repository:** huggingface/pytorch-image-models @ `ae4d1bbfefab7e4f2f49a744838a2d9c7713146d`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated venv and installed a Blackwell-capable CUDA 12.8 PyTorch stack.
2. Ran `repro.py` against the local `codebase/` with synthetic 224x224 CUDA batches and `torch.compile(fullgraph=True, backend="inductor")`.
3. Observed finite losses for both eager and compiled runs; no non-finite loss occurred.

## Observed behavior

- On this machine, with torch 2.7.0+cu128, torchvision 0.22.0+cu128, timm 1.0.22, and an sm_120 Blackwell GPU, both eager and compiled TinyViT training completed 16 steps with finite losses. The compiled path did not produce NaNs; it reported elapsed_s=34.797 versus eager elapsed_s=0.608 in the captured run.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported NaN failure did not reproduce in this environment. The compiled run stayed numerically stable through the full test window.
