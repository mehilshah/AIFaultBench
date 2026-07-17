# Bug 549 Reproduction Bundle

This folder reproduces the `torch.onnx._export` failure reported for `timm`.

## What fails

`timm.utils.onnx.onnx_export()` still calls the private `torch.onnx._export`
API. With Torch 2.6, that symbol is gone, so export raises:

`AttributeError: module 'torch.onnx' has no attribute '_export'`

## Layout

- `repro.py` - minimal Python repro
- `requirements.txt` - runtime dependencies for the repro environment
- `setup_env.sh` - creates a local virtualenv and installs dependencies
- `run_repro.sh` - runs the repro inside the prepared environment
- `manifest.json` - bug metadata

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

Or, with Docker:

```bash
```

The script uses the checked-in `codebase/` directly via `PYTHONPATH`, so the
application source is not modified.
