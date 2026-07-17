# Bug 574

This folder is the reusable standardized benchmark input for the vLLM FP8 KV-cache regression reported in issue `#47037`.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What the repro does:
- Checks whether the local runtime can import `torch` and expose an SM90-class CUDA device.
- If the runtime is capable, it runs the issue reporter's exact `vllm serve` and `lm_eval` commands for `poolside/Laguna-XS.2-FP8`.
- If the runtime is not capable, it exits with a concrete blocker instead of pretending the bug reproduced.

Reproduction command:
`bash run_repro.sh`
