# Reproduction Trajectory — Bug 274: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2712](https://github.com/huggingface/pytorch-image-models/issues/2712)
- **Repository:** huggingface/pytorch-image-models @ `c2819eadc8ff87e59b7c55cd2d8f06bacdcecd42`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed the repro dependencies from requirements.txt.
2. Executed ./run_repro.sh with stdout and stderr captured to repro_stdout.log and repro_stderr.log.
3. Observed AssertionError from repro.py confirming reg_token is missing from no_weight_decay() and group_matcher() for both VisionTransformer and Eva.

## Observed behavior

- Running the repro on the local codebase raises AssertionError because both VisionTransformer and Eva omit reg_token from no_weight_decay() and place reg_token in a different layer-decay group than cls_token. The captured stdout shows reg_token alone in the deepest group with weight_decay 0.05 and lr_scale 1.0, while cls_token stays in the stem group with weight_decay 0.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && ./run_repro.sh >repro_stdout.log 2>repro_stderr.log
```
