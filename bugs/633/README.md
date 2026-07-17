# Bug 633 Reproduction Bundle

This folder reproduces JAX issue 37921: `jnp.searchsorted` returns `int32`
even when `jax_enable_x64=True`.

Contents:
- `bug_report.txt`: original report text
- `codebase/`: local source snapshot used for the repro
- `repro.py`: minimal probe that compares NumPy and JAX dtypes
- `requirements.txt`: runtime dependencies for the repro venv
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the probe and captures logs
- `manifest.json`: bundle metadata
- `reproduction.json`: machine-readable result
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Repro summary:
- NumPy returns `int64` for `searchsorted` on this 64-bit platform.
- JAX returns `int32` for the same inputs with `jax_enable_x64=False`.
- JAX still returns `int32` with `jax_enable_x64=True`.

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```
