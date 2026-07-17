# Bug 643

This folder contains a self-contained reproduction bundle for the Pyro Funsor ELBO regression described in `bug_report.txt`.

## What it does

- Uses the recovered `codebase/` snapshot as the application source.
- Applies only in-process compatibility shims needed to run that snapshot on the current Python 3.12 / Torch 2.x environment.
- Replays the model and guide from `tests/contrib/funsor/test_enum_funsor.py::test_elbo_enumerate_plate_9`.
- Compares `TraceEnum_ELBO(max_plate_nesting=0)` against `TraceEnum_ELBO(max_plate_nesting=1)`.

## Files

- `repro.py`: standalone reproduction entrypoint.
- `requirements.txt`: Python dependencies for the repro environment.
- `setup_env.sh`: creates `.venv` and installs dependencies.
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`.
- `reproduction.json`: machine-readable result written by `repro.py`.

## Run

```bash
bash run_repro.sh
```

## Result in this folder

The current environment does not reproduce the historical mismatch. The measured losses are identical after compatibility shims:

- `expected_loss=2.393253803253174`
- `actual_loss=2.393253803253174`
- `abs_err=0.0`
