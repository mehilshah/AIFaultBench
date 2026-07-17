# Bug 317 Repro Bundle

This directory contains the standardized inputs and the Reproduction artifacts for the Lightning lr-finder checkpoint restore bug.

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

Repro summary:
- issue URL: `https://github.com/Lightning-AI/pytorch-lightning/issues/21757`
- library: `lightning`
- source version: `2.6.2`
- torch runtime used for repro: `2.6.0+cpu`
- result: reproducible

How to run:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro script verifies that a Lightning checkpoint can be loaded manually with `weights_only=False`, then triggers `Tuner.lr_find()`, which fails during the internal checkpoint restore with `_pickle.UnpicklingError` on torch 2.6.
