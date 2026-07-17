# Bug 216

This folder is the reusable standardized benchmark input for this bug.

Reused source inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
- `bash run_repro.sh`

Observed result:
- `datetime.datetime.now().timestamp()` and `datetime.datetime.fromtimestamp(...).timestamp()` do not round-trip under `freeze_time(..., tz_offset=-1)`.
- The mismatch reproduces on `freezegun 0.3.15` from `codebase/`.

Source summary:
- issue URL: `https://github.com/spulec/freezegun/issues/344`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
