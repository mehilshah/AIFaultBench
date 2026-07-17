# Bug 620 Reproduction

This folder reproduces the JAX issue reported at
`https://github.com/jax-ml/jax/issues/37991`.

The failure is in `jnp.cumsum(x, dtype=bool)` for integer input. NumPy casts to
boolean before accumulating, but this JAX checkout accumulates the integers
first and only casts at the end when `dtype` is passed as the Python builtin
`bool`.

Files in this folder:

- `bug_report.txt`: original issue report
- `codebase/`: local JAX checkout used for the repro
- `requirements.txt`: minimal runtime dependency set
- `setup_env.sh`: creates the isolated venv and installs dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr
- `repro.py`: minimal script that prints the NumPy vs JAX results
- `manifest.json`: standardized metadata for the folder
- `reproduction.json`: machine-readable outcome
- `repro_stdout.log` / `repro_stderr.log`: captured command output

Run the repro with:

```bash
bash run_repro.sh
```

Observed result in this environment:

- NumPy returns `[True, True]`
- JAX returns `[True, False]`
- `matches: False`
