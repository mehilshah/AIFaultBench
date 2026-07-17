# Reproduction Bundle

This folder reproduces diffusers issue 13864 in a minimal, source-anchored way.

## What fails

The Cosmos pipeline code at:

- [`codebase/src/diffusers/pipelines/cosmos/pipeline_cosmos2_5_predict.py`](codebase/src/diffusers/pipelines/cosmos/pipeline_cosmos2_5_predict.py)

calls:

- `self.safety_checker.check_text_safety(p)`

If a pipeline instance is incorrectly passed as `safety_checker`, that object has
`to(...)` but no `check_text_safety(...)`, so the call raises `AttributeError`.

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

Or with Docker:

```bash
```

## Expected outcome

The script prints the source marker and then fails with:

`AttributeError: 'Cosmos2_5_PredictBasePipeline' object has no attribute 'check_text_safety'`
