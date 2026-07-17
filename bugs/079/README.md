# RegionViT LayerNorm repro

This folder contains a minimal reproduction for the RegionViT local token
embedding bug reported in lucidrains/vit-pytorch#330.

## What fails

`RegionViT(tokenize_local_3_conv=True)` applies `nn.LayerNorm(init_dim)` to a
tensor in NCHW format. `LayerNorm` expects the normalized dimension to be the
last axis, so the first normalization layer raises a shape mismatch during the
forward pass.

## Reproduction

```bash
bash run_repro.sh
```

Expected result:

- `input_shape=(1, 3, 224, 224)`
- an exception from `torch.nn.LayerNorm`
- non-zero exit status

## Files

- `repro.py` - minimal failing forward pass
- `requirements.txt` - runtime dependencies for the repro
- `setup_env.sh` - creates a virtual environment and installs dependencies
- `run_repro.sh` - one-command entry point
- `manifest.json` - standardized metadata
