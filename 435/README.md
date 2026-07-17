# Bug 435

This folder contains a standalone reproduction bundle for the LTX2 connector
layout regression described in diffusers issue 13930.

Inputs:
- `bug_report.txt`
- `codebase/` checked out at `41add3410424cc33d748a7fd3409132d2f6b4ad2`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- the connector layout in `codebase/src/diffusers/pipelines/ltx2/connectors.py` uses masked write plus `torch.flip`
- the issue report's toy example shows that this reverses prompt tokens and register tiles
- the repro script encodes that same toy example and asserts the mismatch
