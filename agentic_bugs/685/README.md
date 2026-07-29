# Bug 685

Reproduction bundle for https://github.com/langchain-ai/langchain/issues/38717.

**PIIMiddleware: PIIMatch not exported from public package, and docs use wrong field names for custom detectors**

## What is checked

The public `PIIMatch` import failure reproduces deterministically with `langchain==1.2.12`. The runner intentionally exits 1 only when the reported ImportError is observed. All requested reproduction artifacts and captured logs are present.

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
