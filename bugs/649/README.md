# Bug 649

Reproduction bundle for https://github.com/run-llama/llama_index/issues/21422.

**[Bug]: LLMChatEndEvent.model_dump() mutates ChatResponse.raw in-place, corrupting caller's response object**

## What is checked

The issue reproduces without an LLM client, API key, or network call. Serializing LLMChatEndEvent mutates the caller-owned ChatResponse.raw from a Pydantic model to a dict; all required reproduction artifacts are present.

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
