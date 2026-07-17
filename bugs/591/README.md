# Bug 591

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/pyro-ppl/pyro/issues/2886`
- commit hash: `ced727e579c50654bdf264604652d93fe663c0d5`
- library: `pyro`
- library version: `1.6.0`
- status: reproducible here with `python3.9` and `torch==1.9.0+cpu`

Recommended local flow:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

Notes:
- The repro uses the local `codebase/` checkout via `PYTHONPATH`.
- The historical Pyro checkout expects a torch 1.x runtime; this bundle pins a CPU wheel for torch 1.9.0.
