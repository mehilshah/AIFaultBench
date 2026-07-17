# Bug 383

This folder is the reusable standardized benchmark input for the timm FSDP bug.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

## What this repro does

The reported failure is in `torch.distributed.fsdp._fully_shard.fully_shard`, which rejects any `nn.ModuleDict` instance before checking whether the subclass implements `forward()`.

`timm.create_model("convnextv2_base", features_only=True)` returns `FeatureListNet`, which inherits from `nn.ModuleDict` and does implement `forward()`. The repro exercises that exact path and captures the `ValueError`.

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

## Notes

The exact high-level `FullyShardedDataParallel(..., ShardingStrategy.FULL_SHARD)` constructor path also requires a non-CPU accelerator in this environment. The underlying bug is still reproducible through `fully_shard(FeatureListNet)`, which hits the same offending validation.
