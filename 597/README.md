# Bug 597

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

Reproduction:
1. Run `bash setup_env.sh`.
2. Run `bash run_repro.sh`.

Observed result:
- The repro script captures the missing `flops_per_batch` warning twice over a 2-step `Trainer.fit` run.
- That result is written to `reproduction.json`.

Source summary:
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21450`
- commit hash: `027455bcd9433f201b1136f68d54b1a07588abe3`
- library: `pytorch-lightning`
- library version: `2.6.0`
