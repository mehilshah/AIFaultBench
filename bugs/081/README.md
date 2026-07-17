# Bug 081 Reproduction Bundle

This bundle reproduces `vit-pytorch` issue 304 from the local `codebase/` checkout.

## Bug Summary

`CrossViT` assumes 3-channel images when building its patch embedding layer. Passing a 1-channel image produces a `LayerNorm` shape mismatch during the forward pass.

## Files

- `bug_report.txt`: original issue description
- `codebase/`: local source checkout used for reproduction
- `repro.py`: minimal Python repro
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: install dependencies
- `run_repro.sh`: execute the repro
- `manifest.json`: metadata for this bundle

## Reproduction

Run:

```bash
bash run_repro.sh
```

The script exercises `CrossViT` with a `1 x 1 x 256 x 256` tensor and reproduces the runtime error from the bug report.
