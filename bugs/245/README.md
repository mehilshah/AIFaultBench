# Bug 245 Reproduction Bundle

This folder reproduces the `numpyro` import-time `DeprecationWarning` reported in
[`bug_report.txt`](./bug_report.txt).

## What fails

Importing `numpyro` with `jax==0.8.2` reaches:

`numpyro/ops/provenance.py -> from jax.interpreters.pxla import xla_pmap_p`

That import emits:

`DeprecationWarning: jax.interpreters.pxla.xla_pmap_p is deprecated as of JAX v0.8.2.`

The repro script promotes `DeprecationWarning` to an error so the failure is
easy to detect in automation.

## Files

- `repro.py`: minimal import-only repro
- `requirements.txt`: dependency pins for the repro environment
- `setup_env.sh`: create and populate a local virtual environment
- `run_repro.sh`: run the repro and capture logs
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log`, `repro_stderr.log`: captured run output

## Run

```bash
bash run_repro.sh
```

The command exits non-zero because the warning is raised as an error.
