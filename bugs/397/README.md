# Bug 397

This folder is a self-contained reproduction bundle for the ViT seed/reproducibility report.

Contents:
- `bug_report.txt`
- `codebase/` cloned at `cebc007d66041fee4e468305065872ec1200bec2`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro harness runs a tiny local ViT training job twice with the same seed and once with a different seed. In this environment, the same-seed runs match exactly, so the reported nondeterminism is not reproducible here.
