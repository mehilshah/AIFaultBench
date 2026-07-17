# Bug 636

This folder is the reusable standardized benchmark input for Lightning issue 21428.

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

Current snapshot result:
- The reported ordering is not reproducible on this codebase snapshot.
- Observed sequence: `optimizer_step` happens before `on_validation_epoch_end`.

Run:
- `bash run_repro.sh`
