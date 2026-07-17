# Reproduction Trajectory — Bug 056: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1672](https://github.com/keras-team/keras-io/issues/1672)
- **Repository:** keras-team/keras-io @ `cbe83d8244cb53e0a42299b8b5da4c460c6ae768`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a uint8 image tensor and resize it with `ops.image.resize(ops.convert_to_tensor([image]), size=(72, 72))`.
2. Pass the resized tensor into the Vision Transformer `Patches` layer from the example.
3. Observe the Conv2D dtype mismatch traceback from `keras.ops.image.extract_patches`.

## Observed behavior

- Running `bash run_repro.sh` with `keras==3.0.0` and `tensorflow-cpu==2.16.1` prints `resized_dtype=<dtype: 'int32'>` and then fails in `Patches.call()` with `InvalidArgumentError: cannot compute Conv2D as input #1(zero-based) was expected to be a int32 tensor but is a float tensor [Op:Conv2D]`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
