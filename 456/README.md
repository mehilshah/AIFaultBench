# Bug 456

This folder contains a minimal reproduction bundle for the timm 1.0.18
Python 3.9 import-time failure.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- issue URL: `https://github.com/huggingface/pytorch-image-models/issues/2555`
- commit hash: `e6ab6bc3c6f40b5a9600051309eb5b1933845501`
- library: `timm`
- version: `1.0.18`
- root cause: `def nullwrap(fn: F | None = None)` is evaluated at import time on Python 3.9, which raises a `TypeError`

Run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`
