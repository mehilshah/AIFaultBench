# Reproduction Bundle

Bug: `ErnieImageTransformer2DModel` does not implement `from_single_file`.

## Files

- `repro.py`: minimal runtime repro
- `setup_env.sh`: creates an isolated venv and installs a CPU-only torch wheel plus the minimal runtime deps
- `run_repro.sh`: runs the repro and captures stdout/stderr into `repro_stdout.log` and `repro_stderr.log`
- `manifest.json`: machine-readable summary of the repro

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

## Expected result

The script prints that `from_single_file` is missing and then raises:

`AttributeError: type object 'ErnieImageTransformer2DModel' has no attribute 'from_single_file'`
