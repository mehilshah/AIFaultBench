# Bug 730

Reproduction bundle for https://github.com/microsoft/semantic-kernel/issues/13148.

**.Net: Bug: .NET AddHuggingFaceEmbeddingGenerator return 404**

## What is checked

Reproduced the .NET Hugging Face embedding-generator bug offline. The report’s Kernel.CreateBuilder().AddHuggingFaceEmbeddingGenerator path constructs a request to the obsolete api-inference.huggingface.co endpoint; the deterministic stub returns 404 and Semantic Kernel raises HttpOperationException. All required reproduction files and captured logs are present.

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
