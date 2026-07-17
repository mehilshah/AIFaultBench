# Bug 431

This folder is the reusable standardized benchmark input for this bug.

Reused inputs:
- `bug_report.txt`
- `codebase/` at commit `7c574997e9027edce53820b5f38134fb3e5d05c0`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- Install the lightweight metadata-only dependency set.
- Run `repro.py`, which loads SDV from the local checkout without importing the full package tree.
- The script asserts that removing `table2.fk_1` should leave the `table1 -> table3` relationship intact.
- On this codebase, the assertion fails because both relationships are removed.

Usage:
1. `bash setup_env.sh`
2. `bash run_repro.sh`
