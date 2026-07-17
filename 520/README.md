# Bug 520

This folder is a self-contained reproduction bundle for JAX issue 38101.

Observed here with the local `codebase/` checkout plus the pinned runtime
dependencies in `requirements.txt`:

- `jax.jit(jax.vmap(program))(x)` returns `[3.4028235e+38]`
- `jax.vmap(program)(x)` returns `[inf]`

The program is `relu -> square -> sqrt_abs` evaluated at `float32.max`.

Files in this bundle:

- `bug_report.txt`: recovered issue report
- `codebase/`: local source checkout used for the repro
- `repro.py`: minimal failing program
- `requirements.txt`: external runtime dependencies
- `setup_env.sh`: creates a virtualenv and installs the dependencies
- `run_repro.sh`: runs the reproducer
- `manifest.json`: metadata for the standardized folder
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured run output

To reproduce locally:

```bash
bash setup_env.sh
bash run_repro.sh
```

