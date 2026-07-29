# Bug 659

Reproduction bundle for https://github.com/langchain-ai/langgraph/issues/8211.

**with_structured_output is not supported when reasoning effort is used**

## What is checked

Reproduced the external langchain-openai failure without any provider calls or API keys. With reasoning enabled, the mocked Responses API returns the issue's plain-text greeting despite the JSON schema request, and the real OpenAI/Pydantic parsing path raises the asserted invalid-JSON ValidationError. All required reproduction artifacts are present.

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
