# Bug 548

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

Reproduction command:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/47147`
- commit hash: `ea9ddf59fc9d262da7467699959d8c84600c073c`
- inferred library: `vllm`
- inferred library version: `unknown`
- bug report source: `bug_report.txt`
- codebase source: `vllm-project/vllm@ea9ddf59fc9d262da7467699959d8c84600c073c`
- status: non-reproducible here because `AsyncLLM.pause_generation()` already clears the renderer multimodal cache before pausing the engine
