# Bug 006 Reproduction

This folder contains a self-contained reproduction for TensorFlow Models issue `11134`.

## What it does

The repro builds an EfficientNet-B1 backbone from the local `codebase/`, slices it at the same feature tap point used by EfficientDet-style models, and then minimizes a dummy loss while passing the full backbone variable list to the gradient utility.

That causes TensorFlow to warn that some variables have no gradients, which matches the bug report.

## Files

- `repro.py`: minimal Python repro
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: installs dependencies
- `run_repro.sh`: runs the repro
- `manifest.json`: metadata for this standardized bug folder
- `reproduction.json`: machine-readable repro status
- `repro_stdout.log`: captured stdout from the repro run
- `repro_stderr.log`: captured stderr from the repro run

## Expected result

The run should print a warning similar to:

`Gradients do not exist for variables ... when minimizing the loss.`

The validated run in this folder used Python 3.12 with `tensorflow-cpu==2.16.1`
and `tf-keras==2.16.0` inside a local virtualenv.
