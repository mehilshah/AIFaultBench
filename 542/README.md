# Bug 542

Repro for JAX issue `jax.jit + jnp.log + jnp.exp` hiding overflow in `jit(log(exp(x)))`.

Observed here on the local checkout:

- `jit(log(exp(89))) = 89.0`
- `eager log(exp(89)) = inf`

## Files

- `repro.py`: minimal Python reproducer.
- `requirements.txt`: runtime dependencies for the repro venv.
- `setup_env.sh`: creates `.venv` and installs dependencies.
- `run_repro.sh`: runs the repro against the local `codebase/` checkout.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The script intentionally fails with an `AssertionError` once the mismatch is observed.
