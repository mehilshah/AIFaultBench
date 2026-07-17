# Reproduction Trajectory — Bug 009: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11133](https://github.com/tensorflow/models/issues/11133)
- **Repository:** tensorflow/models @ `e923b8aa3b066c02432ffdb7d5fd93d465b6eaa5`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read bug_report.txt and located the TF Object Detection TF2 export path.
2. Inspected codebase/research/object_detection/exporter_lib_v2.py and exporter_main_v2.py for the reported attribute error.
3. Ran bash run_repro.sh and captured stdout/stderr logs.

## Observed behavior

- repro_stdout.log shows that exporter_lib_v2.DetectionFromImageModule has no 'outputs' attribute assignment and exporter_main_v2.py has 0 'outputs' attribute reads.
- repro_stderr.log shows the runtime blocker: No module named 'tensorflow'.
- codebase/research/object_detection/exporter_lib_v2.py:137 defines DetectionFromImageModule as a tf.Module wrapper; code around lines 140-167 sets up __call__ but does not define an outputs property.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

TensorFlow is not installed in this workspace, so the exporter runtime path cannot be executed here.
