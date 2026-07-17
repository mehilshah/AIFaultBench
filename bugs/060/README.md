# Bug 060 Reproduction

This folder reproduces the KerasCV semantic-segmentation failure described in `bug_report.txt`.

## What fails

`keras_cv.layers.RandAugment` is applied to a dictionary containing:

- `images` as `float32`
- `segmentation_masks` as `int64`

When the pipeline is traced through `tf.data.Dataset.map(...)`, `tf.switch_case` inside `RandomChoice` sees branches that return different dtypes for `segmentation_masks`:

- one branch returns `float32`
- another branch returns `int64`

TensorFlow raises:

`TypeError: branches[0] and branches[1] arguments to tf.switch_case must have the same number, type, and overall structure of return values.`

## Files

- `repro.py`: minimal synthetic repro
- `requirements.txt`: pinned runtime deps
- `setup_env.sh`: creates the virtualenv and installs deps
- `run_repro.sh`: runs the repro and captures logs

## Run

```bash
./run_repro.sh
```

The command writes detailed output to:

- `repro_stdout.log`
- `repro_stderr.log`

