# Bug 673

Reproduction bundle for https://github.com/agno-agi/agno/issues/8235.

**[Bug] `AttributeError: 'TeamRunOutput' object has no attribute 'event'` in team SSE streaming**

## What is checked

Reproduced offline. A fake team yields a TeamRunOutput accumulator into the real Team SSE router; the router forwards it to the formatter, which accesses the nonexistent singular `.event` attribute and emits a TeamRunError response.

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
