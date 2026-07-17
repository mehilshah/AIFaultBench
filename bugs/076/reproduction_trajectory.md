# Reproduction Trajectory — Bug 076: Mask_RCNN

- **Bug report:** [https://github.com/matterport/Mask_RCNN/issues/3050](https://github.com/matterport/Mask_RCNN/issues/3050)
- **Repository:** matterport/Mask_RCNN @ `3deaec5d902d16e1daf56b62d5971d428dc920bc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a standalone keras Conv2D layer named conv1 whose weights are keras.src.backend.Variable objects.
2. Wrote a legacy-style HDF5 file with layer_names/weight_names entries for conv1.
3. Called the repository's MaskRCNN.load_weights(..., by_name=True) method against that file.
4. Observed the NotImplementedError from tensorflow.python.keras.saving.hdf5_format._legacy_weights.

## Observed behavior

- MaskRCNN.load_weights() raised NotImplementedError when loading a legacy-format HDF5 file. The observed message was: "Save or restore weights that is not an instance of `tf.Variable` is not supported in h5, use `save_format='tf'` instead."

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
