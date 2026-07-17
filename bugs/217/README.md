# Bug 217

This folder is a self-contained reproduction bundle for Stanza issue 1357.

What it does:
- installs a clean Python 3.11 environment
- installs the local `codebase/` in editable mode
- downloads the Stanza `en/mimic` resources into `stanza_resources/`
- runs the failing pipeline initialization:
  `stanza.Pipeline('en', package='mimic', processors={'ner': 'i2b2'})`

Expected outcome:
- the POS trainer initialization crashes with `KeyError: 'bert_finetune'`

Files:
- `bug_report.txt`: original issue description
- `codebase/`: local Stanza source snapshot
- `repro.py`: minimal repro driver
- `requirements.txt`: Python dependencies for the repro
- `setup_env.sh`: creates and prepares the venv
- `run_repro.sh`: executes the repro and writes logs/result JSON
- `reproduction.json`: schema-constrained result produced by `run_repro.sh`
- `repro_stdout.log`, `repro_stderr.log`: captured command output
