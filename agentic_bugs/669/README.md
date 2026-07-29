# Bug 669

Reproduction bundle for https://github.com/pydantic/pydantic-ai/issues/6611.

**OpenAI background polling requests encrypted content for persisted responses**

## What is checked

Reproduced the persisted OpenAI background-polling failure without provider traffic. The pinned retrieval path sends `reasoning.encrypted_content`; the local fake persisted endpoint returns the reported 400, which Pydantic AI maps to `ModelHTTPError`. All required benchmark artifacts were created.

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
