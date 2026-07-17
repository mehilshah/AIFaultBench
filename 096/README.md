# Bug 096 Repro Bundle

This folder contains a self-contained reproduction attempt for:

- Issue: https://github.com/lucidrains/denoising-diffusion-pytorch/issues/286
- Reported symptom: `RuntimeError: Inference tensors cannot be saved for backward`
- Suspected site: self-conditioning branch in `codebase/denoising_diffusion_pytorch/denoising_diffusion_pytorch.py`

## What the repro does

`repro.py` forces the self-conditioning branch, runs a tiny forward/backward pass, and checks whether the reported runtime error appears.

## Current result

On the available stable torch builds in this folder, the backward pass completes successfully and the reported error does not reproduce.

## How to run

```bash
bash run_repro.sh
```

The run script writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Files

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
