# Bug 394

This folder is the reusable standardized benchmark input for the DeepSpeed ZeRO-0 bf16 gradient-norm bug.

Source inputs:
- `bug_report.txt`
- `codebase/` at `a44fb58f134afc5399b29c154a5502e14272774c`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Setup command:
`bash setup_env.sh`
