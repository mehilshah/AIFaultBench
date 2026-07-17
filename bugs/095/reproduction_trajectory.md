# Reproduction Trajectory — Bug 095: denoising-diffusion-pytorch

- **Bug report:** [https://github.com/lucidrains/denoising-diffusion-pytorch/issues/292](https://github.com/lucidrains/denoising-diffusion-pytorch/issues/292)
- **Repository:** lucidrains/denoising-diffusion-pytorch @ `840d3ffd3b64276250faec2ec612e13847f69894`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` from the bug folder.
2. The harness calls `GaussianDiffusion.ddim_sample()` on a `LearnedGaussianDiffusion` subclass.
3. The inherited call to `self.model_predictions(..., clip_x_start=True, rederive_pred_noise=True)` conflicts with the overridden `model_predictions(self, x, t, clip_x_start=False)` signature and raises `TypeError`.

## Observed behavior

- Running `bash run_repro.sh` triggers `TypeError: LearnedGaussianDiffusion.model_predictions() got multiple values for argument 'clip_x_start'` when the inherited DDIM sampling path passes both a positional `self_cond` and the keyword argument `clip_x_start=True`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
