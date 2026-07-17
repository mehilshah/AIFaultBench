# Bug 555

This folder contains a self-contained repro bundle for JAX issue 38098.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro command:
- `bash ./run_repro.sh`

Observed behavior:
- `jax.jit(jax.grad(lambda x: jnp.sum(jnp.log2(jnp.exp2(x)))))(jnp.array([126.0], dtype=jnp.float32))` returns `[1.]`
- `jax.grad(...)` returns `[0.]`

Issue URL:
- `https://github.com/jax-ml/jax/issues/38098`
