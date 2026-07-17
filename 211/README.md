# Bug 211

This folder contains a self-contained repro bundle for SDV issue 1910.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- `PARSynthesizer` samples float-valued categorical data outside the original categories.
- `run_diagnostic(...).get_details('Data Validity')` reports `CategoryAdherence = 0.0` for the synthetic `category` column.

Run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Issue reference:
- https://github.com/sdv-dev/SDV/issues/1910
