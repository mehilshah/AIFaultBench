# Bug 097 Reproduction Bundle

This folder reproduces the `Missing device in classifier_free_guidance.py` bug from
`lucidrains/denoising-diffusion-pytorch`.

## What fails

`classifier_free_guidance.GaussianDiffusion.q_sample()` uses `self.device` when
`offset_noise_strength > 0`, but `GaussianDiffusion` does not define a `device`
property.

## Repro

1. Install the dependencies:
   ```bash
   bash setup_env.sh
   ```
2. Run the repro:
   ```bash
   bash run_repro.sh
   ```

Expected outcome:
`AttributeError: 'GaussianDiffusion' object has no attribute 'device'`

