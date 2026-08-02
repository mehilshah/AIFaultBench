# Bug 771

Reproduction bundle for https://github.com/huggingface/smolagents/issues/1532.

**[BUG] ChatMessage `content` Attribute Accessed Incorrectly**

## What is checked

The pinned smolagents checkout reproduces issue #1532 without API keys or network calls. A deterministic local model completes an agent run; the managed-agent summary then subscripts ChatMessage and raises the reported TypeError.

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
