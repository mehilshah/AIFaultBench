# Bug 363 Repro

This folder captures a minimal reproduction attempt for the install-time dependency issue described in `bug_report.txt`.

What the repro does:
- creates an isolated virtual environment
- runs a dry-run install of `whisperx==3.4.3`
- records the resolver output in `repro_stdout.log` and `repro_stderr.log`

Current result:
- the issue is **not reproducible** in this environment
- `pip` resolves `whisperx==3.4.3` successfully and includes `lightning-2.6.5`

Files:
- `repro.py`: Python driver for the resolver check
- `requirements.txt`: target package pin used by the report
- `setup_env.sh`: creates the isolated environment
- `run_repro.sh`: runs the repro and captures logs
- `reproduction.json`: structured outcome

