# Bug 332

This folder is the reusable standardized benchmark input for the diffusers attention-processor report.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Observed result in this checkout:
- the custom attention processor wrapper stays attached after a forward pass
- `attn2` processors remain the injected wrapper objects
- the bug reported in issue `#14103` was not reproducible here
