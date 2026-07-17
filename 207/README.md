# Bug 207

This folder is a self-contained reproduction bundle for POT issue 712.

Observed outcome in this checkout:
- `ot.dist(..., metric="minkowski", p=...)` behaves correctly on a 2D input.
- The report's 1D example is not diagnostic because 1D Minkowski distances are identical for all `p`.
- The bug is not reproducible in the checked-out `codebase/` snapshot.

Included artifacts:
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

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```

The repro script inserts `codebase/` into `PYTHONPATH`, so no application code is modified.
