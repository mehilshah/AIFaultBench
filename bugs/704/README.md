# Bug 704

Reproduction bundle for https://github.com/pydantic/pydantic-ai/issues/6051.

**`GoogleModel` never sets `include_server_side_tool_invocations` for `CodeExecutionTool`, so code execution can't be combined with function tools on Gemini 3**

## What is checked

Reproduced offline. GoogleModel omits `include_server_side_tool_invocations` for CodeExecutionTool combined with a function tool, causing the assertion and expected non-zero exit.

## Current result on this host

The issue reproduces on this host.

## Files

- `bug_report.txt`
- `repro.py`
- `requirements.txt`
- `setup_codebase.sh`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `reproduction_trajectory.md`
- `repro_stdout.log` / `repro_stderr.log`
- `manifest.json`, `github.json`

## Run

```bash
bash setup_codebase.sh
bash run_repro.sh
```
