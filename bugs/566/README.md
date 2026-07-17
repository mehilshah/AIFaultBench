# Bug 566

This folder contains the standardized repro bundle for SDV issue 2714.

Inputs reused from the raw benchmark folder:
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
1. `bash run_repro.sh`
2. Inspect `reproduction.json` for the outcome.

Observed result in this environment:
- The reported sample-time `KeyError: 58.0` did not reproduce.
- With the issue's reported context ordering, fit fails earlier in `deepecho` during context type inference.
- With a control ordering that aligns the context vector, fit and sample both succeed.

Source summary:
- issue URL: `https://github.com/sdv-dev/SDV/issues/2714`
- commit hash: `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- codebase version in the checked-in tree: `1.27.1.dev0`
