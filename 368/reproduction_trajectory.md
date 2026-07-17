# Reproduction Trajectory — Bug 368: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2612](https://github.com/huggingface/pytorch-image-models/issues/2612)
- **Repository:** huggingface/pytorch-image-models @ `ae4d1bbfefab7e4f2f49a744838a2d9c7713146d`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Set up a clean virtual environment with CUDA-enabled Torch and the minimal timm dependencies.
2. Run bash run_repro.sh from the standardized bug folder.
3. Inspect repro_stdout.log and repro_stderr.log for the measured timings and warnings.

## Observed behavior

- The local benchmark completed on NVIDIA RTX PRO 6000 Blackwell Max-Q Workstation Edition with Torch 2.9.0+cu128.
- Full ConvNeXt benchmark for convnext_large_in22ft1k reported baseline_seconds=0.009554077095041672 and patched_seconds=0.010003208958854279.
- The baseline/patched ratio was 0.9551012214520361, so the contiguous workaround did not produce the reported slowdown reduction on this host.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The bug report describes a PyTorch-version-dependent slowdown, but the only Torch build that can execute on this Blackwell GPU here (2.9.0+cu128) does not show the regression. Older Torch builds in the 2.5/2.8 line were incompatible with sm_120 on this host, so the reported environment-specific slowdown could not be observed.
