# Bug 694

Reproduction bundle for https://github.com/run-llama/llama_index/issues/21089.

**[Bug]: Refine does not catch `ValueError`/`TypeError` from tool-calling structured outputs**

## What is checked

Reproduced offline with llama-index-core 0.14.18. Refine leaks the structured-output ValueError instead of following its ValidationError fallback path. All required reproduction files and final captured logs are present.

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
