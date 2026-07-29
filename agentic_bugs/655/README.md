# Bug 655

Reproduction bundle for https://github.com/SWE-agent/SWE-agent/issues/1179.

**swe-bench Docker image uses Python 3.5, incompatible with `tree-sitter==0.21.3` required by edit_anthropic**

## What is checked

The pinned installer has unguarded pip commands, so a tree-sitter installation failure aborts tool installation. The offline repro deterministically simulates the documented Python 3.5 incompatibility and confirms the enclosing shell command exits 1. All requested artifacts and captured final output are present.

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
