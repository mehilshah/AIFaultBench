# Bug 118 Reproduction Bundle

This folder contains a standalone reproduction for the dependency-resolution bug reported in:

- `https://github.com/clearml/clearml/issues/1440`

## What fails

`clearml==2.0.0` requires `requests>=2.32.0` on Python 3.8+, while `clearml-agent==1.9.3` requires `requests<=2.31.0`.
Pip cannot satisfy both constraints in the same environment.

## Files

- `requirements.txt`: the conflicting top-level requirements
- `repro.py`: runs the resolver in an isolated virtual environment and writes logs
- `run_repro.sh`: convenience wrapper
- `setup_env.sh`: creates a local helper venv if you want one
- `reproduction.json`: machine-readable result
- `repro_stdout.log` and `repro_stderr.log`: captured output from the failing resolution

## Run

```bash
bash run_repro.sh
```

The script should exit successfully after confirming that pip reports a resolution conflict.
