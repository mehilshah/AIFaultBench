# Bug 746

Reproduction bundle for https://github.com/langchain-ai/langchain/issues/37736.

**EnsembleRetriever: arank_fusion uses different normalization logic than rank_fusion causing ValidationError in async**

## What is checked

Reproduced the async EnsembleRetriever normalization bug using a local deterministic retriever; no provider or network calls occur at runtime. All requested reproduction scripts, dependency pins, logs, metadata, trajectory, and README are present.

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
