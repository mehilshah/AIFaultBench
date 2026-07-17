# Bug 193 Reproduction

This folder contains a self-contained reproduction bundle for Equinox issue 1172.

## What fails

`jax.lax.scan` over a Module carry, combined with `jax.vmap(carry)(x)`, raises:

`TypeError: can only concatenate str (not "_Sentinel") to str`

The minimal trigger is in [`repro.py`](./repro.py).

## Files

- [`bug_report.txt`](./bug_report.txt): source issue description
- [`codebase/`](./codebase): local Equinox checkout under test
- [`requirements.txt`](./requirements.txt): pinned runtime dependencies
- [`setup_env.sh`](./setup_env.sh): creates the virtual environment and installs deps
- [`run_repro.sh`](./run_repro.sh): runs the reproducer and captures logs
- [`reproduction.json`](./reproduction.json): schema-constrained reproduction result
- [`repro_stdout.log`](./repro_stdout.log): stdout from the latest repro run
- [`repro_stderr.log`](./repro_stderr.log): stderr from the latest repro run

## Reproduction

```bash
bash setup_env.sh
bash run_repro.sh
```

Or use the recorded command in `reproduction.json`:

```bash
bash run_repro.sh
```
