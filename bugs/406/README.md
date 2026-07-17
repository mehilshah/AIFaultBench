# Bug 406

Reproduction bundle for diffusers issue 13979.

## What fails

`Ideogram4ModularPipeline` in the pinned codebase inherits only `ModularPipeline`.
The Ideogram-specific LoRA mixin exists in `diffusers/loaders/lora_pipeline.py`, but
it is not mixed into the modular pipeline class, so `load_lora_weights()` is absent.

## Repro

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro uses source inspection rather than model loading, because the local
environment has a broken torch installation that would otherwise block imports.

## Files

- `repro.py`: AST-based repro
- `requirements.txt`: no extra dependencies
- `setup_env.sh`: environment bootstrap
- `run_repro.sh`: runs the repro
- `reproduction.json`: machine-readable result
