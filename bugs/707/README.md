# Bug 707

Reproduction bundle for https://github.com/stanfordnlp/dspy/issues/8996.

**[Bug] LiteLLM exception when using OpenAI Speech-To-Text models**

## What is checked

Created all required benchmark files and captured a final deterministic offline run. The pinned client routes transcription-only models through LiteLLM chat completion by design, so this issue is not reproducible as a code defect without making an invalid provider request.

## Current result on this host

The issue did not reproduce here. The reported BadRequestError is an unsupported-endpoint mismatch, not an executable fault: gpt-4o-mini-transcribe requires OpenAI's audio transcription endpoint while the pinned DSPy LM supports chat, text, and responses endpoints only.

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
