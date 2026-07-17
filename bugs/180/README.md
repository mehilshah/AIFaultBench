# Bug 180

This folder contains a standalone reproduction bundle for
`LightningCLI`-related mixed-import callback validation.

What is included:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction flow:
1. Create the virtual environment and install dependencies with `./setup_env.sh`
2. Run `./run_repro.sh`

The repro intentionally mixes `lightning.pytorch` with `pytorch_lightning` and
passes a callback class, which hits the bad `_check_mixed_imports()` path and
raises `ValueError: Expected a parent`.
