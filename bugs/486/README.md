# Bug 486

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

Reproduction command:
`bash setup_env.sh && bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/accelerate/issues/1200`
- commit hash: `e4620984f8f2d3b91585f7d8c03f8c57cd453f50`
- inferred library: `accelerate`
- inferred library version: `0.18.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `huggingface/accelerate@e4620984f8f2d3b91585f7d8c03f8c57cd453f50`
