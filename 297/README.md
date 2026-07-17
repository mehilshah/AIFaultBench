# Reproduction Bundle

This bundle reproduces the `uv sync` failure reported for `torch_geometric`
with the PyG wheel index configuration from issue 10629.

## What it does

The bundled `pyproject.toml` matches the report:

- `torch==2.8.0`
- `torchvision>=0.23.0`
- `torch_geometric`
- `tool.uv.find-links` points at `https://data.pyg.org/whl/torch-2.8.0+cu128.html`
- `torch_geometric` is sourced from the `pyg` index

## Expected result

Running `bash run_repro.sh` should fail during dependency resolution with an
error stating that `torch-geometric` was not found in the package registry and
that the PyG index URL returned `403 Forbidden`.

## Files

- `pyproject.toml`: minimal resolver input
- `repro.py`: runs the reproduction command
- `run_repro.sh`: executes the repro and writes `repro_stdout.log` and
  `repro_stderr.log`
- `setup_env.sh`: installs `uv` if it is missing
