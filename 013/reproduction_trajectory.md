# Reproduction Trajectory — Bug 013: tensorflow-models

- **Bug report:** [https://github.com/tensorflow/models/issues/11087](https://github.com/tensorflow/models/issues/11087)
- **Repository:** tensorflow/models @ `1900bc561292177818dfb73946474e79078098ff`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set Matplotlib backend to svg before importing the target module.
2. Execute codebase/official/vision/utils/object_detection/visualization_utils.py with minimal import stubs for TensorFlow and unrelated official modules.
3. Observe that the backend changes to Agg immediately after module import.

## Observed behavior

- Loading the real source file codebase/official/vision/utils/object_detection/visualization_utils.py switches Matplotlib from svg to Agg during import. That file contains an import-time matplotlib.use('Agg') call, which is the same side effect reached transitively from tensorflow_models.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
