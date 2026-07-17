# Bug 333

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

The issue report is about a GitHub tag being force-pushed, so the repro bundle checks the local snapshot and confirms whether Git metadata is available to inspect tag history.

Source summary:
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21740`
- commit hash: `5f98958cb133c0b9e50831cc4f66ced2404c6729`
- inferred library: `pytorch-lightning`
- inferred library version: `2.6.2`
- bug report source: `bug_report.txt`
- codebase source: `Lightning-AI/pytorch-lightning@5f98958cb133c0b9e50831cc4f66ced2404c6729`
