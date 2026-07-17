# Bug 587

This folder is the reusable standardized benchmark input for this bug.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

What the repro checks:
- `response_format` is converted into structured-output constraints.
- `enable_thinking` is only injected from reasoning settings, not from `response_format`.
- The local runtime probe currently stops earlier because the installed Torch/NCCL stack is inconsistent in this workspace.

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/47027`
- commit hash: `3483240b7ea3d4372b6c79369ea36617f8b1fbb2`
