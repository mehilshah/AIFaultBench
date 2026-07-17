# Bug 134

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/flairNLP/flair/issues/3684`
- library: `flair`
- observed failure: `ImportError: cannot import name 'WIKINER_FRENCH' from 'flair.datasets'`
- reproduction command: `bash run_repro.sh`
