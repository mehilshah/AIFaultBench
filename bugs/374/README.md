# Reproduction Bundle

This folder reproduces the ModelNet10 download failure reported in
https://github.com/pyg-team/pytorch_geometric/issues/10396.

## What fails

`torch_geometric.datasets.ModelNet(".../modelnet10", "10", True)` attempts to
download:

`http://vision.princeton.edu/projects/2014/3DShapeNets/ModelNet10.zip`

That URL returns `HTTP Error 404: Not Found`.

## Files

- `repro.py`: minimal Python driver that instantiates `ModelNet`.
- `requirements.txt`: runtime dependencies for the isolated repro environment.
- `setup_env.sh`: creates `.venv` and installs the pinned runtime stack.
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` and
  `repro_stderr.log`.
- `manifest.json`: bug metadata for the standardized bundle.
- `reproduction.json`: schema-constrained verdict.

## Run

```bash
./run_repro.sh
```
