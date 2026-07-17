# Bug 423

This folder contains a local repro bundle for Accelerate issue #1489.

What the repro checks:
- the CLI parser in this revision does not expose `--rdzv_backend`
- the same setting is accepted through a YAML config file
- the multi-node launch path therefore falls back to the default `static` rendezvous backend

Files:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `repro_worker.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
