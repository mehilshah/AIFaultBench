# Bug 508 Reproduction Bundle

This folder reproduces NumPyro issue 2053, where importing `numpyro` on a clean
environment fails because `typing_extensions` is imported but not declared as a
runtime dependency.

Artifacts in this folder:
- `bug_report.txt`: recovered issue report
- `codebase/`: local NumPyro snapshot used for reproduction
- `requirements.txt`: minimal runtime dependencies for the repro environment
- `setup_env.sh`: creates an isolated virtual environment and installs deps
- `repro.py`: imports `numpyro` and surfaces the failure
- `run_repro.sh`: convenience wrapper that sets up the env and runs the repro
- `manifest.json`: metadata for the standardized folder
- `reproduction.json`: schema-constrained result written after verification
- `repro_stdout.log`, `repro_stderr.log`: command output captured during repro

Run:
```bash
bash run_repro.sh
```
