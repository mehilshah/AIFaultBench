# Bug 093 Repro

This folder contains a self-contained repro bundle for x-transformers issue 228.

## What fails

The bundled run currently completes successfully in this checkout, so the standardized
environment does not reproduce the original tensor shape mismatch reported in issue 228.

## Files

- `repro.py` - minimal failing script
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - creates `.venv` and installs dependencies
- `run_repro.sh` - sets up the environment and runs the reproducer
- `reproduction.json` - structured result
- `repro_stdout.log` / `repro_stderr.log` - captured output from the failing run

## Reproduce

```bash
./run_repro.sh
```
