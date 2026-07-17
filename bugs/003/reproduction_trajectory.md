# Reproduction Trajectory — Bug 003: models

- **Bug report:** [https://github.com/tensorflow/models/issues/13495](https://github.com/tensorflow/models/issues/13495)
- **Repository:** tensorflow/models @ `4e7462990b0e4313ecebdfa8100e51d80925cca1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment and install tensorflow==2.18.0 from requirements.txt.
2. Set PYTHONPATH to codebase/research so the local object_detection package is imported.
3. Run repro.py via run_repro.sh to import object_detection.core.freezable_sync_batch_norm.

## Observed behavior

- bash run_repro.sh exited with code 1.
- repro_stdout.log shows tensorflow_version=2.18.0 and has_tf_keras_layers_experimental=False.
- The import fails with AttributeError: module 'keras._tf_keras.keras.layers' has no attribute 'experimental'.
- repro_stderr.log traceback points to codebase/research/object_detection/core/freezable_sync_batch_norm.py:20.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
