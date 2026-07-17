# Bug 322

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

Reproduction summary:
- `import timm` fails when `DeprecationWarning` is treated as an error.
- The traceback points to `codebase/timm/models/hrnet.py:521` and `@torch.jit.interface`.
