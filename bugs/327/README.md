# Bug 327

This folder contains a self-contained repro bundle for SDV issue 2855.

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

Reproduction summary:
- issue URL: `https://github.com/sdv-dev/SDV/issues/2855`
- library: `sdv`
- observed version: `1.35.1.dev0`
- status: reproducible
- symptom: `run_diagnostic` reports a score of `0.75` because synthesized datetime values fall outside the real data range
