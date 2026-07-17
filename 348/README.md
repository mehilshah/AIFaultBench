# Bug 348

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
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21703`
- commit hash: `78bf0214a0ad7571391619dca952c13988c0dc51`
- inferred library: `pytorch-lightning`
- inferred library version: `2.6.2`
- bug report source: `bug_report.txt`
- codebase source: `Lightning-AI/pytorch-lightning@78bf0214a0ad7571391619dca952c13988c0dc51`

Repro sequence:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro uses the local source tree via `PYTHONPATH=codebase/src` and exercises `Trainer.predict()` with a spawned multiprocessing `DataLoader` and `persistent_workers=True`.
