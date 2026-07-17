# Bug 458

This folder contains a standalone repro for:
`https://github.com/pytorch/rl/issues/3508`

What reproduces:
`PrioritizedSampler(...)` raises `RuntimeError: SumSegmentTreeFp32 is not available. See warning above.`

Repro steps:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Artifacts in this folder:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
