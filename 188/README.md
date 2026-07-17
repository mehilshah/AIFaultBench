# Bug 188

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

Source summary:
- issue URL: `https://github.com/meta-pytorch/torchtune/issues/2828`
- library: `torchtune`
- library version: `0.7.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

How to run:
- `bash ./run_repro.sh`

Expected outcome:
- `set_list_to_stack(False)` succeeds.
- `set_list_to_stack(True)` raises `KeyError: tensor(10)` while converting `RequestOutput`.
