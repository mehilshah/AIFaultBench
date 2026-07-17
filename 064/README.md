# Bug 064

This folder contains a minimal reproduction bundle for the Keras NER Transformer TFLite shape mismatch described in `bug_report.txt`.

Files in this folder:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

What the repro does:
- Builds the transformer NER model from the example architecture.
- Saves it as a TensorFlow SavedModel.
- Converts it to TFLite.
- Shows that the exported TFLite model fixes the token dimension to `1`.
- Attempts to pass a 9-token input and hits the same `Dimension mismatch` failure reported in the issue.

The bundle uses Docker with `python:3.10-slim` and `tensorflow==2.13.0` so the historical SavedModel/TFLite behavior is preserved.
