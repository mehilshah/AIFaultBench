# Bug 689

Reproduction bundle for https://github.com/langchain-ai/langgraph/issues/6782.

**graph.invoke() / graph.stream() raise AttributeError when config is not a mapping**

## What is checked

The reported invalid-config behavior reproduces deterministically. Passing a string config to `graph.invoke()` triggers the internal AttributeError instead of config validation. All required reproduction files and final captured logs are present.

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
