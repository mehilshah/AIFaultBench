# Bug 270 Repro Bundle

This bundle targets [huggingface/accelerate#3877](https://github.com/huggingface/accelerate/issues/3877):
gradient accumulation was reported to change the loss curve when using DeepSpeed ZeRO-2.

## What is included

- `repro.py`: the TRL SFT training script adapted from the issue report.
- `ds_zero2.yaml`: the DeepSpeed ZeRO-2 Accelerate config used by the repro.
- `run_repro.sh`: runs two comparable configurations and records the observed loss gap.
- `setup_env.sh`: creates a local venv and installs the tested dependency set.

## Observed result here

On this machine, the reported SFT path did **not** reproduce the loss divergence.

- `batch_size=2, gradient_accumulation_steps=4`: `train_loss=11.920878887176514`
- `batch_size=8, gradient_accumulation_steps=1`: `train_loss=11.920918822288513`
- Absolute difference: about `3.99e-05`

That is within normal floating-point noise for this short run.

## How to run

1. Install the dependencies with `bash setup_env.sh`.
2. Run `bash run_repro.sh`.
3. Check `reproduction.json`, `repro_stdout.log`, and `repro_stderr.log`.

## Notes

- The bundle uses CUDA 12.8 PyTorch wheels because this machine has an `sm_120` Blackwell GPU.
- The issue report used `wandb`, but the bundle disables external tracking so the loss path is isolated.
