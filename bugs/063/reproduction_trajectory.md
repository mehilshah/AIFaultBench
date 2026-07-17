# Reproduction Trajectory — Bug 063: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1512](https://github.com/keras-team/keras-io/issues/1512)
- **Repository:** keras-team/keras-io @ `aaefb6d40b4da79b3450e5cbf65155cbea49434b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build the Docker image with `bash setup_env.sh`.
2. Run `bash run_repro.sh`.
3. Observe the tf.switch_case dtype mismatch inside keras_cv.layers.RandAugment.

## Observed behavior

- Running the augmentation stack from the Oxford Pets segmentation example inside Docker (python:3.10-slim-bookworm, tensorflow==2.13.1, keras-cv==0.6.1, keras-core==0.1.5) fails while tracing tf.data.Dataset.map(...). The error is: TypeError: branches[0] and branches[1] arguments to tf.switch_case must have the same number, type, and overall structure of return values; segmentation_masks are returned as both float32 and int64.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
