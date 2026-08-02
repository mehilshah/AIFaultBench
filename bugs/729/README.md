# Bug 729

Reproduction bundle for https://github.com/microsoft/semantic-kernel/issues/13298.

**Python: Bug: Fix import path: microsoft.agents vs microsoft_agents**

## What is checked

Reproduced the import-path defect using the released semantic-kernel 1.37.0 package. Importing CopilotStudioAgent fails before any API call because it imports nonexistent `microsoft.agents` instead of `microsoft_agents`.

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
