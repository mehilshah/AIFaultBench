# Bug 749

Reproduction bundle for https://github.com/langchain-ai/langgraph/issues/6576.

**Pydantic error when using custom tool node and having runtime in the tools**

## What is checked

The reported failure reproduces offline without any LLM or provider calls. A custom-style `tool.invoke({})` call omits LangGraph's injected ToolRuntime, causing the expected Pydantic ValidationError.

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
bash setup_codebase.sh && bash run_repro.sh
```
