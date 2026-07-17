# PyG legacy `Data` pickle repro

This folder reproduces the reported failure from
`pytorch_geometric` issue 10497.

## What it does

`repro.py` creates a `torch_geometric.data.Data` object, removes its internal
`_store` field to mimic an older PyG pickle payload, writes it to
`legacy_data.pkl`, loads it back, and prints the object.

Printing the object triggers `Data.__repr__`, which accesses `_store` and raises
the reported RuntimeError:

`The 'data' object was created by an older version of PyG.`

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local venv and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: machine-readable metadata

## Run locally

```bash
./run_repro.sh
```

## Expected result

The script prints the loaded object type and then exits with the legacy PyG
RuntimeError from `torch_geometric/data/data.py`.
