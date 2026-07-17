# Bug 553

This folder contains the reproducible SDV bug bundle for issue #2716.

Inputs:
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

Observed result:
- `PerformanceAlert` prints the exact huge column count instead of a capped `1000000+` display.

Reproduction command:
- `bash run_repro.sh`
