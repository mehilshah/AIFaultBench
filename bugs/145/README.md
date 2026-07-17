# Bug 145

This folder is the reusable standardized benchmark input for this bug.

Observed behavior:
- `StaticEmbedding.from_distillation("BAAI/bge-base-en-v1.5", device="cuda")`
  runs successfully in this environment.
- The example similarity is `tensor([[0.5375]])`, not the docstring value
  `tensor([[0.9177]])`.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Quick start:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/sentence-transformers/issues/3175`
- commit hash: `not found in Dataset.csv`
- inferred library: `sentence-transformers`
- inferred library version: `3.4.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
