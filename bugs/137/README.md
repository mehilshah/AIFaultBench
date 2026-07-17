# Bug 137

This folder contains a reproducible benchmark bundle for the ROUGE multilingual tokenizer issue.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction:
1. Run `bash run_repro.sh`
2. The default ROUGE call on identical Nepali strings returns all zeros.
3. The same inputs with `tokenizer=str.split` return `1.0` for all ROUGE variants.

Source summary:
- issue URL: `https://github.com/huggingface/evaluate/issues/564`
- library: `evaluate`
- library version: `0.4.2.dev0`
