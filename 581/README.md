# Bug 581

This folder contains a reproducible JAX gradient mismatch from
https://github.com/jax-ml/jax/issues/38096.

Reproduction summary:
- `jax.jit(jax.grad(f))(x)` returns `[1.]`
- `jax.grad(f)(x)` returns `[inf]`
- `x = jnp.array([1.1754944e-38], dtype=jnp.float32)`

Files:
- `bug_report.txt`: original issue description
- `codebase/`: local JAX source tree
- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a venv and installs dependencies
- `run_repro.sh`: runs the repro inside the prepared environment
- `reproduction.json`: machine-readable reproduction result
- `repro_stdout.log` and `repro_stderr.log`: captured command output

Run:
```bash
bash run_repro.sh
```
