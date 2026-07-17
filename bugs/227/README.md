# Bug 227 Repro Bundle

This folder contains a self-contained reproduction of POT issue 229.

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
- issue URL: `https://github.com/PythonOT/POT/issues/229`
- library: `POT`
- library version: `0.7.0`
- observed behavior: `ot.emd` returns a feasible plan with cost `354.43787279000003`, while the manual plan `Q` has cost `57.54321038317501`
