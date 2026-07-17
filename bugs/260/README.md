# Bug 260 Reproduction Bundle

This folder reproduces the SDV multi-table constraint bug described in `bug_report.txt`.

## Summary

- Issue: overlapping `Inequality` constraints on the same table in `HMASynthesizer`
- Observed failure: `ConstraintNotMetError: Table 'parent' is missing columns 'colB'.`
- Repro status: reproducible in the local `codebase/`

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the reproducer
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the reproducer
- `reproduction.json`: schema-constrained result summary
- `repro_stdout.log`, `repro_stderr.log`: captured command output

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The reproducer uses the local source tree via `PYTHONPATH=codebase`.
