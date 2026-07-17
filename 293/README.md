# Reproduction Bundle

This bundle reproduces the NumPyro import failure reported in issue 2174.

## What it does

`repro.py` imports `numpyro` from the local `codebase/`. With `jax==0.10.0`, the import chain reaches `numpyro/ops/provenance.py`, which tries to import `xla_pmap_p` from `jax.extend.core.primitives`.

## Run

```bash
bash run_repro.sh
```

## Files

- `repro.py`: minimal failing script
- `requirements.txt`: dependency list
- `setup_env.sh`: local virtualenv setup
- `run_repro.sh`: executes the repro
- `manifest.json`: bundle metadata
