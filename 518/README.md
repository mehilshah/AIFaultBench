# Bug 518 Reproduction Bundle

This folder reproduces SDV issue 2736: adding single-table constraints to a multi-table synthesizer in multiple steps breaks `fit()`.

## What reproduces

The minimal repro uses a tiny custom multi-table schema:
- `parent` table with two independent inequality pairs
- `child` table linked by a foreign key

Control case:
- add both constraints in one `add_constraints()` call
- `fit()` succeeds

Bug case:
- add the same constraints in two separate `add_constraints()` calls
- `fit()` fails with `InvalidDataError`

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates and populates the local virtualenv
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: schema-constrained result summary

## Run

```bash
bash run_repro.sh
```

