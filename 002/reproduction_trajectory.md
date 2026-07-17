# Reproduction Trajectory — Bug 002: models

- **Bug report:** [https://github.com/tensorflow/models/issues/13517](https://github.com/tensorflow/models/issues/13517)
- **Repository:** tensorflow/models @ `1bdb87d92d40e8f63285dafb6803139e25a59baf`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a TensorFlow 2.17.1 virtual environment from `requirements.txt`.
2. Ran `python repro.py` through `run_repro.sh`.
3. Observed the expected `ModuleNotFoundError` from `from tensorflow.contrib.quantize.python import graph_matcher`.

## Observed behavior

- Running `bash run_repro.sh` with TensorFlow 2.17.1 prints the legacy import reference from `codebase/research/object_detection/exporter.py` and then fails with `ModuleNotFoundError: No module named 'tensorflow.contrib'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
