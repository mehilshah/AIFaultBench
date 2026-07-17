# Bug 275

This folder is a self-contained repro bundle for Detectron2 issue 4915.

## What fails

Scripting a Mask R-CNN model and saving the scripted module raises:

`RuntimeError: Could not export Python function call 'is_fx_tracing'`

The traceback points at [`codebase/detectron2/modeling/poolers.py`](codebase/detectron2/modeling/poolers.py).

## Repro

Run:

```bash
bash run_repro.sh
```

The wrapper will:

1. Create a local virtualenv in `.venv/` if needed.
2. Install the pinned runtime dependencies from `requirements.txt`.
3. Add `codebase/` to `PYTHONPATH`.
4. Execute [`repro.py`](repro.py), which builds a Mask R-CNN model from the local config and calls `torch.jit.save()` on the scripted module.

## Expected result

The command fails with the `is_fx_tracing` TorchScript export error.

## Notes

- The repro uses a small runtime patch for `PIL.Image.LINEAR` because newer Pillow releases removed that alias.
- The local source tree is left untouched.
