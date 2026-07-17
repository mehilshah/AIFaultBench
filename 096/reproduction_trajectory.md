# Reproduction Trajectory — Bug 096: denoising-diffusion-pytorch

- **Bug report:** [https://github.com/lucidrains/denoising-diffusion-pytorch/issues/286](https://github.com/lucidrains/denoising-diffusion-pytorch/issues/286)
- **Repository:** lucidrains/denoising-diffusion-pytorch @ `242e4b63dad7d5d9d0bf4f465f861f98dfba918d`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Installed a local virtualenv and the minimal dependency set needed by the package.
2. Forced the self-conditioning branch by patching the module-level random() helper to return 0.0.
3. Ran a tiny GaussianDiffusion forward/backward pass with self_condition=True.
4. Observed that loss.backward() completed successfully, so the reported bug did not reproduce in this environment.

## Observed behavior

- A forced self-conditioning forward/backward pass completed successfully. On torch 2.13.0+cpu and torch 2.9.1+cpu, the script printed status=backward_completed instead of raising RuntimeError: Inference tensors cannot be saved for backward.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

Not reproducible here on the available stable torch builds; the reported inference-mode autograd failure did not occur.
