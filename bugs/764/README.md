# Bug 764

Reproduction bundle for https://github.com/langflow-ai/langflow/issues/11792.

**make docker_build failing- ModuleNotFoundError: No module named 'hatchling.build'**

## What is checked

Created all required reproduction artifacts. The focused isolated build exercises the reported hatchling backend and confirms the error does not occur with a clean cache on this host.

## Current result on this host

The issue did not reproduce here. The reported ModuleNotFoundError depends on a corrupted uv/Podman build cache. With uv 0.9.1 and a fresh isolated cache, the pinned langflow-base source builds successfully, so the absent external corrupted cache state cannot be reproduced deterministically on this machine.

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
