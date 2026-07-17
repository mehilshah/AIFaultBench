# Reproduction Trajectory — Bug 383: pytorch-image-models

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2609](https://github.com/huggingface/pytorch-image-models/issues/2609)
- **Repository:** huggingface/pytorch-image-models @ `ae4d1bbfefab7e4f2f49a744838a2d9c7713146d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create a clean venv with torch 2.6.0+cpu and the local timm source installed editable.
2. Run `bash run_repro.sh` to execute `repro.py` and capture stdout/stderr into `repro_stdout.log` and `repro_stderr.log`.
3. Observe that the script prints `model_type=FeatureListNet` and fails with the reported `ValueError` from torch's `fully_shard` guard.

## Observed behavior

- `repro.py` creates `FeatureListNet` via `timm.create_model("convnextv2_base", pretrained=False, features_only=True)`, prints `model_type=FeatureListNet`, and then `fully_shard(encoder)` raises `ValueError: fully_shard does not support containers that do not implement forward`. The timm class defines `forward()` at `codebase/timm/models/_features.py:344-345`, but torch rejects it at `_fully_shard.py:145-148` purely because it inherits `nn.ModuleDict`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
