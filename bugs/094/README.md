# Bug Reproduction Bundle

Issue: [`norm.gamma not used during backprop`](https://github.com/lucidrains/PaLM-rlhf-pytorch/issues/46)

This folder contains a minimal repro harness for the local checkout in `codebase/`.

## What was tested

- Plain forward/backward on a tiny `PaLM` model
- CPU `DistributedDataParallel` with `world_size=1`

## Outcome

The reported unused-parameter failure was **not reproducible** in this environment.

Observed results:

- `layers.0.fn.norm.gamma` had a non-`None` gradient
- `layers.1.fn.norm.gamma` had a non-`None` gradient
- `norm.gamma` had a non-`None` gradient
- CPU DDP backward completed without error

## Repro command

```bash
bash run_repro.sh
```

The command is also recorded in `reproduction.json`.
