# Bug 143

This folder is the reusable standardized benchmark input for this issue.

Issue summary:
- URL: `https://github.com/huggingface/sentence-transformers/issues/3043`
- Library: `sentence-transformers`
- Library version: `3.3.0.dev0`
- Reported symptom: offline reload after saving a `trust_remote_code=True` Nomic model fails because `configuration_hf_nomic_bert.py` cannot be found.

What is included:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Current result in this folder:
- Not reproducible on the checked-in codebase.
- The save step persists `configuration_hf_nomic_bert.py` and `modeling_hf_nomic_bert.py`, and a fresh offline reload succeeds.

How to run:
1. `./setup_env.sh`
2. `./run_repro.sh`
3. Inspect `repro_stdout.log`, `repro_stderr.log`, and `reproduction.json`
