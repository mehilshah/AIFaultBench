# Bug 274 Reproduction Bundle

This folder reproduces the `reg_token` grouping/weight-decay bug reported for `timm`.

## What is reproduced

- `VisionTransformer.no_weight_decay()` omits `reg_token`
- `VisionTransformer.group_matcher()` omits `reg_token`
- `Eva.no_weight_decay()` omits `reg_token`
- `Eva.group_matcher()` omits `reg_token`

The repro uses small locally instantiated models, so it does not need pretrained weights.

## Files

- `repro.py` - standalone repro script
- `requirements.txt` - runtime dependencies
- `setup_env.sh` - installs dependencies
- `run_repro.sh` - executes the repro
- `manifest.json` - metadata for the standardized bundle
- `reproduction.json` - structured result from the repro run

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is expected to fail with an assertion showing that `reg_token` is not treated like `cls_token`.
