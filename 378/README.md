# Bug 378

This folder contains the reproduction bundle for Lightning issue `#21692`.

Observed outcome in this workspace:
- The checked-in `codebase/` is a clean source tree.
- The malicious import-time `_runtime` chain described in the upstream report is not present here.
- Running `python3 repro.py` reports `not reproducible in this checkout`.

Relevant upstream report:
- `https://github.com/Lightning-AI/pytorch-lightning/issues/21692`

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally:
```bash
bash run_repro.sh
```
