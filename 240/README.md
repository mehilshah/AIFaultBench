# NumPyro Bug 240 Repro Bundle

This folder contains a self-contained reproduction bundle for:

- issue: `tracer error in blocked AutoGuide`
- upstream report: `https://github.com/pyro-ppl/numpyro/issues/1753`
- local codebase: `codebase/`

What the repro does:

1. Installs a compatible JAX stack into a local virtualenv.
2. Installs the checked-out `numpyro` codebase in editable mode.
3. Runs two `SVI.init` calls under `jax.vmap`:
   - a baseline model that succeeds
   - a model with `numpyro.deterministic("test", a)` that raises `UnexpectedTracerError`

Files:

- `repro.py` - minimal Python reproducer
- `requirements.txt` - runtime dependencies for the repro
- `setup_env.sh` - creates the local virtualenv and installs dependencies
- `run_repro.sh` - runs the reproducer and writes logs
- `manifest.json` - metadata for this bundle
- `reproduction.json` - schema-constrained result generated after verification
- `repro_stdout.log` / `repro_stderr.log` - captured run output

Usage:

```bash
bash setup_env.sh
bash run_repro.sh
```

The deterministic-site case is reproducible in this checkout with:

- Python `3.12.3`
- `jax==0.4.38`
- `jaxlib==0.4.38`
- `numpyro==0.13.2` from `codebase/`
