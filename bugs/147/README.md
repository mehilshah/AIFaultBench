# Bug 147

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro command:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/sentence-transformers/issues/3325`
- library: `sentence-transformers`
- library version: `4.1.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
- repro approach: a synthetic `SentenceTransformer` subclass drives the real `encode()` implementation into the `output_value=None` prompt path without downloading a remote model
