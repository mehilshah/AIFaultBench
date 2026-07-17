# Bug 261

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

Source summary:
- issue URL: `https://github.com/stanfordnlp/stanza/issues/1423`
- commit hash: `not found in Dataset.csv`
- inferred library: `stanza`
- inferred library version: `1.9.2`
- bug report source: `bug_report.txt`
- runtime source: `stanza==1.9.2` from PyPI

Reproduction:
- set up the isolated environment with `bash setup_env.sh`
- run the repro with `bash run_repro.sh`
- the failing case is the Portuguese sentence containing `exemplo1.com, exemplo2.com e exemplo3.com.br`
