# Bug 603

Reproduction bundle for NumPyro issue 2008, "potential mach ports leakage".

Files in this folder:
- `bug_report.txt`: original issue report
- `codebase/`: local NumPyro snapshot used for reproduction
- `repro.py`: synthetic reproduction script
- `requirements.txt`: minimal runtime dependencies
- `setup_env.sh`: creates an isolated virtualenv and installs dependencies
- `run_repro.sh`: wrapper that runs the repro under the prepared environment
- `manifest.json`: standardized metadata for this folder
- `reproduction.json`: final reproduction verdict
- `repro_stdout.log` / `repro_stderr.log`: captured output from the repro run

The original report depends on a macOS-specific Mach-port symptom, but the local run still exercises the same SVI/model pattern and shows steady RSS growth on Linux.
