# Bug 392

This folder captures a reproducibility attempt for the PyPI package `lightning==2.6.3`.

Observed state in this workspace:
- The Lightning git checkout at `codebase/` is clean and does not contain the reported `_runtime` payload.
- The live index no longer serves `lightning==2.6.3`, so the exact malicious wheel cannot be downloaded here today.

Artifacts in this folder:
- `repro.py`: static and network-backed checks for the reported wheel layout
- `requirements.txt`: target package pin from the report
- `setup_env.sh`: minimal Python environment bootstrap
- `run_repro.sh`: wrapper that captures stdout/stderr into logs
- `manifest.json`: metadata for this standardized bug folder
- `reproduction.json`: machine-readable reproduction outcome
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Primary reproduction command:
```bash
bash run_repro.sh
```

Expected result in this workspace:
- `lightning==2.6.3` cannot be fetched from PyPI, so the repro is blocked by artifact availability.

