# Bug 687

Reproduction bundle for https://github.com/langchain-ai/langchain/issues/38629.

**MultiQueryRetriever.unique_union() crashes on list/dict metadata**

## What is checked

Not reproduced on this machine. The offline repro passes list-valued document metadata to the real `MultiQueryRetriever.unique_union()` path and it deduplicates successfully instead of raising `TypeError: unhashable type: 'list'`. Required scripts, logs, metadata, trajectory, and README were created.

## Current result on this host

The issue did not reproduce here. The matching released package for the pinned checkout already uses equality-based deduplication, so list-valued metadata is never hashed and the reported TypeError cannot occur.

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
