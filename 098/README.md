# Bug Reproduction

This folder contains a minimal reproduction for the `SinusoidalPosEmb` bug from
`denoising_diffusion_pytorch/denoising_diffusion_pytorch.py`.

## What fails

`SinusoidalPosEmb.forward()` references `theta` without storing it on `self`.
Calling the layer raises:

`NameError: name 'theta' is not defined`

## How to run

```bash
bash run_repro.sh
```

## Files

- `repro.py`: extracts the buggy class from the local codebase and calls it.
- `run_repro.sh`: wrapper used for reproduction.
- `setup_env.sh`: no-op setup script for completeness.
- `manifest.json`: metadata for the repro bundle.
