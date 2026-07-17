# Reproduction Bundle

This folder reproduces the Masked Patch Prediction dimension mismatch reported in `bug_report.txt`.

## What fails

`vit_pytorch.mpp.MPP.forward()` applies `transformer.to_patch_embedding[-1]` to raw flattened patches. For `ViT`, the last layer in `to_patch_embedding` is `LayerNorm(dim)`, so the input shape is `[batch, patches, 3072]` while the layer expects `1024`.

## Run

```bash
bash run_repro.sh
```

## Expected result

The run terminates with:

```text
RuntimeError: Given normalized_shape=[1024], expected input with shape [*, 1024], but got input of size[20, 64, 3072]
```

## Files

- `repro.py` - minimal failing script
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - creates and populates `.venv`
- `run_repro.sh` - executes the repro
- `manifest.json` - bundle metadata
