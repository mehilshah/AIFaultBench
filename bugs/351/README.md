# Bug 351

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

Run the repro locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

What the repro checks:
- `ResponsesRequest.parallel_tool_calls` accepts `null`/`None`
- `ResponsesResponse.parallel_tool_calls` rejects `null`/`None`
- the mismatch reproduces the 500-triggering validation failure described in `bug_report.txt`

Source summary:
- issue URL: `https://github.com/vllm-project/vllm/issues/48097`
- commit hash: `ab7961a14a59be9a0170f1654315d5c2be44c015`
- inferred library: `vllm`
- inferred library version: `0.23.1rc1.dev878+g47513b91a`
- bug report source: `bug_report.txt`
- codebase source: `vllm-project/vllm@ab7961a14a59be9a0170f1654315d5c2be44c015`
