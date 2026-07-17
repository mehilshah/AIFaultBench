# Bug 330

This folder reproduces JAX issue 39089: a `jit` fastpath cache miss for PRNG key outputs on a multi-device `NamedSharding`.

What to run:

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro script imports the local `codebase/` tree through `PYTHONPATH`, sets `jax_num_cpu_devices=2`, and checks for the reported cache-size transition:

- sharded PRNG key: `1 -> 1 -> 2`
- controls: stay at `1`
- `jax.no_tracing()` raises on the fastpath-produced key

Reproduction artifacts:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:

- issue URL: `https://github.com/jax-ml/jax/issues/39089`
- commit hash: `4f484c50b83d2f7bc779b23a37cd851409324e78`
- bug report source: `bug_report.txt`
- local package source: `codebase/`
