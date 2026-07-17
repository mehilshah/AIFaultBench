# Bug 644

Reproduction bundle for SDV issue 2700.

Bug summary:
- `DayZSynthesizer.create_parameters` raises `KeyError: None` when called with empty `pd.DataFrame()` and empty `Metadata()`.

Files in this folder:
- `bug_report.txt`: recovered issue report
- `codebase/`: local source snapshot used for reproduction
- `repro.py`: minimal script that triggers the bug
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates a local virtual environment and installs requirements
- `run_repro.sh`: runs the repro script and records stdout/stderr
- `manifest.json`: machine-readable metadata for the bundle
- `reproduction.json`: structured reproduction result
- `repro_stdout.log`: captured stdout from the repro run
- `repro_stderr.log`: captured stderr from the repro run

Repro command:
`./run_repro.sh`
