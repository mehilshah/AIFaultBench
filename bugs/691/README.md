# Bug 691

Reproduction bundle for https://github.com/langchain-ai/langgraph/issues/6675.

**calling `model_dump()` on pydantic state variables drops `tool_calls` in AIMessage**

## What is checked

Reproduced the Pydantic serialization failure offline. An AIMessage keeps tool_calls when dumped directly, but loses them when serialized through a `list[BaseMessage]` Pydantic state field; all required benchmark artifacts were written.

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
