# Bug 154

This folder contains a self-contained reproduction bundle for the TVP config bug.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro command:
`bash setup_env.sh && bash run_repro.sh`

What it exercises:
- creates `TvpConfig` without `type_vocab_size`
- constructs `TvpModel(config)`
- hits `AttributeError: 'TvpConfig' object has no attribute 'type_vocab_size'`
