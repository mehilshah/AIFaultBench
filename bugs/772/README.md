# Bug 772

Reproduction bundle for https://github.com/huggingface/smolagents/issues/1518.

**[BUG] smolagents returns 422 if using OpenAIServerModel as the model, with deepinfra as the provider.**

## What is checked

The pinned OpenAIServerModel sends structured list content by default, which DeepInfra-compatible validation rejects with a 422-class error. The reproduction uses a local strict fake client—no API key or network call—and confirms the documented flattening workaround changes content to a string.

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
