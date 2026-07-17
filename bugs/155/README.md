# Bug 155

This folder is the reusable standardized benchmark input for this bug.

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

To reproduce this bug in the folder directly:

`bash run_repro.sh`

Observed result:
- `ImportError: cannot import name 'ALLOWED_LAYER_TYPES' from 'transformers.configuration_utils'`

Source summary:
- issue URL: `https://github.com/huggingface/transformers/issues/43009`
- commit hash: `not found in Dataset.csv`
- inferred library: `transformers`
- inferred library version: `5.0.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`
