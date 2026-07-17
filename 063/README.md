# Bug 063 Reproduction

This folder contains a standalone reproduction bundle for
[`keras-team/keras-io#1512`](https://github.com/keras-team/keras-io/issues/1512).

## What fails

The Oxford Pets segmentation example builds this augmentation pipeline:

- `RandomFlip`
- `RandomRotation(..., segmentation_classes=NUM_CLASSES)`
- `RandAugment(value_range=(0, 1), geometric=False)`

When that pipeline is traced through `tf.data.Dataset.map(...)`, `RandAugment`
raises a `tf.switch_case` dtype mismatch between `float32` and `int64` values for
`segmentation_masks`.

The failing source location in the local codebase is:

- [`codebase/examples/vision/oxford_pets_image_segmentation.py`](codebase/examples/vision/oxford_pets_image_segmentation.py#L150)

## Reproduction

The repo is self-contained through Docker because the host Python version is not
compatible with the TensorFlow pin needed for this bug.

Run:

```bash
bash run_repro.sh
```

That command:

1. Builds a Docker image from [`Dockerfile`](Dockerfile).
2. Runs [`repro.py`](repro.py) inside the container.
3. Captures stdout/stderr in `repro_stdout.log` and `repro_stderr.log`.

## Pinned environment

- `tensorflow==2.13.1`
- `keras-cv==0.6.1`
- `keras-core==0.1.5`

