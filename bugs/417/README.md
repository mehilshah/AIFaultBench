# Bug 417

This folder contains the standardized reproduction bundle for SDV issue 2823.

Inputs:
- `bug_report.txt`
- `codebase/` at commit `b895858c1e306b64f5debf7adc78bdb2b9c78131`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Result:
- The reported nested-list error message is not reproducible in this checkout.
- The actual exception is `InvalidMetadataError: 'primary_key' must be a string.`
