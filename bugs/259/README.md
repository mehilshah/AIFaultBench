# Bug 259

This folder is a self-contained repro bundle for SDV issue 2473.

Observed failure:
- `PARSynthesizer.fit()` succeeds.
- `PARSynthesizer.sample()` raises `KeyError: "['all_null_col'] not in index"` when the training table contains an all-null column that is still declared as a modeled sdtype.

Files in this bundle:
- `bug_report.txt`: original issue report
- `codebase/`: local checkout used for reproduction
- `repro.py`: deterministic reproducer
- `requirements.txt`: runtime dependencies for the repro venv
- `setup_env.sh`: local environment bootstrap
- `run_repro.sh`: wrapper that runs the repro and writes logs/result JSON
- `manifest.json`: standardized bug metadata

To run locally:
`bash run_repro.sh`

