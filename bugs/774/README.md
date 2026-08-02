# Bug 774

Reproduction bundle for https://github.com/browser-use/browser-use/issues/4073.

**Browser Use doesn't works on Windows**

## What is checked

Completed all required reproduction artifacts. The actual BrowserProfile validator is exercised with a fixed UUID and Windows path adapter, reproducing the reported WinError 183 without browser, LLM, API keys, or network calls.

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
