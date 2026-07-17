# Bug 540

This folder is a self-contained repro bundle for SDV issue 2719.

Contents:
- `bug_report.txt`: original bug report
- `codebase/`: local source checkout used for reproduction
- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the repro venv
- `setup_env.sh`: creates the venv and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: machine-readable metadata for the bundle
- `reproduction.json`: final repro verdict
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Reproduction summary:
- `PARSynthesizer.fit()` crashes when `context_columns` are passed in a different order than the underlying data / metadata.
- The observed failure here is `TypeError: the resolved dtypes are not compatible with add.reduce`.

Run locally:
`bash setup_env.sh && bash run_repro.sh`
