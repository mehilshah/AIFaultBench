# Bug 140 Repro Bundle

This folder reproduces the `safetensors` Python slice-indexing bug reported in issue 439.

## What fails

`safe_open("test.st", framework="pt", device="cpu").get_slice("test")[0, :]`
raises:

`TypeError: argument 'slices': failed to extract enum Slice ('Slice | Slices')`

## Files

- `repro.py`: runs the exact repro and writes `reproduction.json`
- `requirements.txt`: runtime Python dependencies for the repro
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` and `repro_stderr.log`
- `manifest.json`: bundle metadata
- `reproduction.json`: machine-readable reproduction result

## Run

```bash
bash run_repro.sh
cat reproduction.json
```
