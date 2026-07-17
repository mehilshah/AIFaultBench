# Reproduction Trajectory — Bug 060: keras-cv

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1583](https://github.com/keras-team/keras-io/issues/1583)
- **Repository:** keras-team/keras-io @ `bd6963345e520ab8b2cbf5894645ab070514aae1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a synthetic tf.data.Dataset element with float32 images and int64 segmentation_masks.
2. Apply keras_cv.layers.RandAugment in a traced Dataset.map pipeline that mirrors the reported notebook pattern.
3. Iterate the dataset; tracing fails inside keras_cv.src.layers.preprocessing.random_choice.RandomChoice with mismatched segmentation_masks dtypes.

## Observed behavior

- Running RandAugment on a synthetic tf.data pipeline with float32 images and int64 segmentation_masks raises TypeError from tf.switch_case: branches[0] and branches[1] must have the same return structure, with segmentation_masks reported as float32 in one branch and int64 in another.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
