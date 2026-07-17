# Reproduction Trajectory — Bug 638: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7686](https://github.com/deepspeedai/DeepSpeed/issues/7686)
- **Repository:** microsoft/DeepSpeed @ `df59f203f40c8a292dd019ae68c9e6c88f107026`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local venv with `./setup_env.sh`.
2. Run `./run_repro.sh` to execute `repro.py` against the local DeepSpeed source snapshot.
3. Observe the crash in `ZenFlowSelectiveAdamW_stage3.group_step()` when `narrow()` is called on a scalar `ds_tensor`.

## Observed behavior

- Running the bundle repro on a CPU-only venv reaches the exact DeepSpeed failure: `RuntimeError: narrow() cannot be applied to a 0-dim tensor`. The traceback points to `codebase/deepspeed/ops/adam/zenflow_torch_adam.py:427` in `ZenFlowSelectiveAdamW_stage3.group_step()`, and the repro prints `param.ds_shape=(3072, 1024)` with `param.ds_tensor.shape=()`. See `repro_stderr.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
