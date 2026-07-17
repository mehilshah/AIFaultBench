# Reproduction Trajectory — Bug 097: denoising-diffusion-pytorch

- **Bug report:** [https://github.com/lucidrains/denoising-diffusion-pytorch/issues/262](https://github.com/lucidrains/denoising-diffusion-pytorch/issues/262)
- **Repository:** lucidrains/denoising-diffusion-pytorch @ `7558d3f59962a9287bd524c464b2edef0e6fae76`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtual environment with `bash setup_env.sh`.
2. Run `bash run_repro.sh` from the bug folder.
3. Observe the missing-`device` `AttributeError` in the output logs.

## Observed behavior

- Running the repro prints `has_device_property=False` and then catches `AttributeError: 'GaussianDiffusion' object has no attribute 'device'` from `classifier_free_guidance.py` when `offset_noise_strength > 0`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
