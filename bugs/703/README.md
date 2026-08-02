# Bug 703

Reproduction bundle for https://github.com/pydantic/pydantic-ai/issues/6081.

**Bedrock: an attachment (`DocumentUrl`/`ImageUrl`) merged into the same user message as a `tool_result` → Converse `ValidationException`**

## What is checked

The fault reproduces deterministically offline. Bedrock message mapping merges a tool result with the next document-bearing user prompt, producing `['toolResult', 'text', 'document']` and causing the repro to exit non-zero.

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
