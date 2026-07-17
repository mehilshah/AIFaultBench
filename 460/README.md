# Bug 460

This folder is the reusable standardized benchmark input for this bug.

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

Source summary:
- issue URL: `https://github.com/pyro-ppl/pyro/issues/3181`
- commit hash: `685c7adee65bbcdd6bd6c84c834a0a460f2224eb`
- inferred library: `pyro`
- inferred library version: `1.8.4+685c7ade`
- bug report source: `bug_report.txt`
- codebase source: `pyro-ppl/pyro@685c7adee65bbcdd6bd6c84c834a0a460f2224eb`

Reproduction status:
- the exact assertion from the issue report passed in both a modern PyTorch environment and in a Python 3.9 environment pinned to `torch==1.13.1`
- the reported mismatch was not observed in this checkout
