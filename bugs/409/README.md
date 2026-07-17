# Bug 409

DeepSpeed import emits a `DeprecationWarning` from `@torch.jit.script` when `torch==2.10.0` is installed.

## Reproduction

```bash
bash setup_env.sh
bash run_repro.sh
```

## What the repro does

- Creates a local dependency directory.
- Installs `torch==2.10.0`.
- Runs `repro.py` with `PYTHONPATH=.deps:codebase`, which turns `DeprecationWarning` into an error and imports `DeepSpeedEngine`.

## Observed result

The import fails at `src_codebase/deepspeed/moe/sharded_moe.py:4` because `torch.jit.script` raises:

`DeprecationWarning: torch.jit.script is deprecated. Please switch to torch.compile or torch.export.`
