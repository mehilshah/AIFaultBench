# Bug 138 Repro Bundle

This folder reproduces the `convnext_tiny.fb_in22k` batch-size dependence reported in:

`https://github.com/huggingface/pytorch-image-models/issues/2244`

## What was observed

With the local `codebase/` checked out here and a CUDA-capable PyTorch stack, the same sample produces different outputs when run as part of a batch versus alone in `eval()` mode.

Captured evidence:

- `batch_out[0][0] = -1.4428796768188477`
- `single_out[0][0] = -1.4428775310516357`
- `abs_diff = 2.1457672119140625e-06`
- `max_abs_diff = 1.6242265701293945e-05`
- `allclose_default = False`

## Files

- `repro.py` - minimal reproduction script
- `requirements.txt` - Python dependencies for the repro environment
- `setup_env.sh` - creates `.venv` and installs dependencies
- `run_repro.sh` - runs the repro and captures logs
- `manifest.json` - standardized metadata
- `reproduction.json` - schema-constrained result payload
- `repro_stdout.log` / `repro_stderr.log` - captured command output

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro expects a CUDA-capable GPU. If CUDA is unavailable, the script exits with a clear error.
