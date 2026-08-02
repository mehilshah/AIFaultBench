# Bug 710

Reproduction bundle for https://github.com/camel-ai/camel/issues/3422.

**[BUG] ChatAgent.__init__() got an unexpected keyword argument 'single_iteration'**

## What is checked

The pinned CAMEL `ChatAgent` constructor rejects the `single_iteration` keyword forwarded by the reported OASIS integration. The deterministic offline repro raises the exact reported TypeError before any model backend or provider API call is made.

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
