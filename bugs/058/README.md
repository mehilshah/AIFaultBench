# Bug 058

RetinaNet training crashes on an empty-box batch in KerasCV 0.6.4 / TensorFlow
2.14.1 with:

`InvalidArgumentError: indices[1,896] = 0 is not in [0, 0)`

This folder is the reusable standardized benchmark input for this bug.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`
