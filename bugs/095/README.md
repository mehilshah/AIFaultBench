# Bug 095 Reproduction

This folder contains a minimal reproduction for the `learned_gaussian_diffusion`
DDIM sampling bug from `denoising-diffusion-pytorch`.

## What fails

`GaussianDiffusion.ddim_sample()` forwards both a positional `self_cond`
argument and a keyword `clip_x_start=True` to `self.model_predictions()`.

`LearnedGaussianDiffusion.model_predictions()` only accepts
`(x, t, clip_x_start=False)`, so the inherited DDIM path raises:

`TypeError: ... got multiple values for argument 'clip_x_start'`

## Files

- `repro.py`: minimal failing harness
- `run_repro.sh`: executes the repro and captures logs
- `setup_env.sh`: environment bootstrap placeholder
- `requirements.txt`: empty because the repro is pure stdlib
- `manifest.json`: metadata for this benchmark folder
- `repro_stdout.log` / `repro_stderr.log`: captured run output

## Run

```bash
bash run_repro.sh
```
