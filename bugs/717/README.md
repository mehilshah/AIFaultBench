# Bug 717

Reproduction bundle for https://github.com/SWE-agent/SWE-agent/issues/1012.

**UnicodeEncodeError in Python Logging: Handling Emojis with cp1252 Encoding Issue**

## What is checked

Reproduced the SWE-agent logging bug without an LLM or network service. The pinned helper omits an explicit file encoding; under the reported cp1252 default, logging `🤖 MODEL INPUT` raises the observed UnicodeEncodeError and the log file remains unwritten.

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
