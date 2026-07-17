# Reproduction Trajectory — Bug 300: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/14117](https://github.com/huggingface/diffusers/issues/14117)
- **Repository:** huggingface/diffusers @ `72eb60c2dad62e44777b5344f21705c6d47bf97f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Warm the cache with a normal `bash run_repro.sh` first-phase download.
3. Run the offline second-phase download with `HF_HUB_OFFLINE=1` and observe the `OSError` failure.

## Observed behavior

- Online `DiffusionPipeline.download('google/ddpm-cifar10-32')` succeeded, but the second call in a fresh process with `HF_HUB_OFFLINE=1` failed with `OSError: Cannot load model google/ddpm-cifar10-32: model is not cached locally...` after `OfflineModeIsEnabled` was raised while fetching metadata from the Hub.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
