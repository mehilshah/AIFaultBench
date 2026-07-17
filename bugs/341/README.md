# Bug 341

This folder contains a standalone reproduction bundle for NumPyro issue 2132.

Observed result in this environment:
- The reported slowdown was **not reproducible**.
- On GPU, the same-object post-warmup run was slightly faster or roughly equal to the fresh `num_warmup=0` restart.

Files in this bundle:
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

Usage:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`
3. Inspect `reproduction.json` and the log files

Reproduction command:
- `bash run_repro.sh`
