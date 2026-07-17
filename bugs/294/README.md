# Bug 294 Reproduction

This folder reproduces the Pyro bug described in `bug_report.txt`.

## Reported failure

`pyro.render_model()` can raise `KeyError: 'constraint'` when a `PyroModule`
uses constrained `PyroParam`s under `module_local_params=True`.

## Files

- `repro.py`: runs the minimal reproducer and writes `reproduction.json`
- `requirements.txt`: external Python dependencies for the repro
- `setup_env.sh`: installs the dependencies
- `run_repro.sh`: executes the repro and captures stdout/stderr

## Reproduction

Run:

```bash
bash run_repro.sh
```

The expected outcome in this snapshot is a `KeyError: 'constraint'` for
`module_local_params=True`, while `module_local_params=False` succeeds.
