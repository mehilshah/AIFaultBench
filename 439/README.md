# Bug 439

This folder contains the raw bug report, the referenced vLLM source checkout, and a minimal repro bundle.

Inputs:
- `bug_report.txt`
- `codebase/` at commit `d63c8e944481e057d00dfee20bc49544d291e521`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction note:
- The bug is WSL2-specific in the report. This bundle reproduces the same `RuntimeError: UVA is not available` path by forcing the pin-memory-off branch that vLLM uses on WSL2 when pinned memory is unavailable.

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/47387`
- commit hash: `d63c8e944481e057d00dfee20bc49544d291e521`
- inferred library: `vllm`
- inferred library version: `0.24.0`
- bug report source: `bug_report.txt`
- codebase source: `vllm-project/vllm@d63c8e944481e057d00dfee20bc49544d291e521`
