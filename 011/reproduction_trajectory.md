# Reproduction Trajectory — Bug 011: models

- **Bug report:** [https://github.com/tensorflow/models/issues/11121](https://github.com/tensorflow/models/issues/11121)
- **Repository:** tensorflow/models @ `e4afd05425bc5a6a74e1b1163cdeacd2e7437174`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Installed the bytecode loader for the bundled tensorflow/models snapshot.
2. Generated local TFRecord training and validation data.
3. Ran ImageClassificationTask with resnet_rs_imagenet-style settings for 100 steps.
4. Observed exploding but finite loss values instead of NaN.

## Observed behavior

- The 100-step run completed without NaN.
- Training loss exploded into the billions but stayed finite through step 100.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

In this Python 3.11 + TensorFlow 2.20 environment, the bundled snapshot does not reproduce the reported NaN loss. The run stays finite and finishes 100 training steps; the behavior differs from the issue report.
