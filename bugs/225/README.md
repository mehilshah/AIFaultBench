# Bug 225

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

Source summary:
- issue URL: `https://github.com/unclecode/crawl4ai/issues/1442`
- commit hash: `not found in Dataset.csv`
- inferred library: `Crawl4AI`
- inferred library version: `0.7.4`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

Repro summary:
- `repro.py` builds a tiny FastAPI app that reuses `codebase/deploy/docker/auth.py`
- no Authorization header returns `200`, which demonstrates the JWT bypass
- invalid tokens return `401`
