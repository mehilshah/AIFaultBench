# Bug 310

This folder contains a self-contained repro bundle for the Pyro `PyroModule` / `torch.nn.ModuleList` nesting bug described in `bug_report.txt`.
In this checkout the issue is already fixed, so the repro completes successfully.

## Contents

- `repro.py`: minimal script that triggers the failure
- `requirements.txt`: Python dependencies needed by the repro
- `setup_env.sh`: creates a venv and installs the pinned dependencies
- `run_repro.sh`: runs the repro and captures logs
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log` and `repro_stderr.log`: captured output from the last run

## Repro command

```bash
./run_repro.sh
```

The observed behavior in this checkout is:

```text
BUG_NOT_REPRODUCED
```
