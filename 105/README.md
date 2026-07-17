# Bug 105 Repro Bundle

This folder contains a standalone reproduction attempt for
`lucidrains/vector-quantize-pytorch` issue 142.

## Contents

- `bug_report.txt` - recovered issue report
- `codebase/` - local source snapshot used for the repro
- `repro.py` - executable harness for the issue configuration
- `requirements.txt` - runtime dependencies for the harness
- `setup_env.sh` - creates a local virtual environment and installs deps
- `run_repro.sh` - runs the repro harness and captures logs
- `manifest.json` - metadata for this standardized bundle
- `reproduction.json` - machine-readable reproduction outcome
- `repro_stdout.log` / `repro_stderr.log` - output captured from the latest run

## Result

The default single-process stress run completed without raising the reported
`shape mismatch` error, so the bug was not reproducible in this environment.
