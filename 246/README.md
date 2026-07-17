# Bug 246

This folder is a self-contained reproduction bundle for the Pyro rendering bug described in `bug_report.txt`.

## What it shows

`pyro.render_model(..., render_params=True)` renders the parameter for a probabilistic model, but omits the same parameter when it only feeds `pyro.deterministic(...)`.

## Files

- `repro.py`: runs the reproduction and prints the rendered graphs.
- `requirements.txt`: minimal runtime dependencies.
- `setup_env.sh`: creates a local virtual environment and installs dependencies.
- `run_repro.sh`: runs the repro script inside that environment.
- `manifest.json`: metadata for the standardized bundle.
- `reproduction.json`: structured result from the last run.
- `repro_stdout.log`, `repro_stderr.log`: captured command output.

## Reproduction command

`bash run_repro.sh`
