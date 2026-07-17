# Bug 010 Repro

This folder reproduces the `validation_loss == 0.0` behavior reported for Model Garden segmentation eval.

## What the repro checks

- `official/vision/tasks/maskrcnn.py` returns `logs = {self.loss: 0}` in `validation_step()`.
- `official/vision/tasks/semantic_segmentation.py` returns `loss = 0` whenever `validation_data.resize_eval_groundtruth` is `False`.
- `official/core/base_trainer.py` copies that task loss into the `validation_loss` metric during eval.

## Run

1. Install dependencies: `bash setup_env.sh`
2. Execute the repro: `bash run_repro.sh`

The script writes the primary output to `repro_stdout.log` and stderr to `repro_stderr.log`.

## Expected output

`repro.py` prints a JSON object containing both validation losses. In this folder, both are `0.0`, which matches the bug report.
