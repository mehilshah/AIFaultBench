# Bug 720

Reproduction bundle for https://github.com/browser-use/browser-use/issues/4510.

**Bug: `action` field returned as JSON string instead of list when done-text contains newlines (Claude Sonnet)**

## What is checked

The pinned Anthropic structured-output parser rejects a nested `action` JSON string containing a literal newline, reporting that `action` is not a list. The offline repro uses no API keys, provider calls, or browser and deterministically captures the failure.

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
