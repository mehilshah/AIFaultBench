# Bug 568 Reproduction Bundle

This folder reproduces the JAX gradient mismatch reported in `bug_report.txt`.

Observed behavior in this snapshot:
- `jax.jit(jax.grad(lambda x: jnp.sum(jnp.log(jnp.exp(x)))))(jnp.array([89.0], dtype=jnp.float32))` returns `[1.]`
- eager `jax.grad(...)` returns `[nan]` for `x=89.0`
- the same pattern appears at `x=88.0` with eager returning `[0.]`

Files:
- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the local source checkout
- `setup_env.sh`: creates and populates `.venv`
- `run_repro.sh`: runs the reproducer and writes `repro_stdout.log` / `repro_stderr.log`
- `manifest.json`: bundle metadata
- `reproduction.json`: schema-constrained result record

Run:
```bash
./run_repro.sh
```

