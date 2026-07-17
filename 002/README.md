# Bug 002 Reproduction

This folder reproduces the TensorFlow 2.x failure reported in
[`bug_report.txt`](./bug_report.txt).

The relevant legacy dependency is in
[`codebase/research/object_detection/exporter.py`](./codebase/research/object_detection/exporter.py),
which references `tensorflow.contrib.quantize.python.graph_matcher`. TensorFlow 2
does not ship `tensorflow.contrib`, so the import fails under a TF2 runtime.

## Files

- `repro.py`: minimal reproduction
- `requirements.txt`: runtime dependency pin
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `repro_stdout.log` and `repro_stderr.log`: captured output from the latest run

## Run

```bash
bash run_repro.sh
```

The expected failure is:

`ModuleNotFoundError: No module named 'tensorflow.contrib'`
