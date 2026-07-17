# Bug 285 Reproduction Bundle

This folder contains a minimal repro for Lightning issue [#21804](https://github.com/Lightning-AI/pytorch-lightning/issues/21804).

## Trigger

The bug occurs when:

1. `Fabric` runs FSDP on CPU.
2. `state_dict_type="full"` is used.
3. Saving a checkpoint enters `_get_full_state_dict_context()`, which unconditionally sets `offload_to_cpu=True`.

## Files

- `repro.py`: minimal reproducer.
- `requirements.txt`: runtime dependencies used by the repro environment.
- `setup_env.sh`: creates the venv and installs dependencies.
- `run_repro.sh`: executes the reproducer.
- `reproduction.json`: machine-readable outcome after running the repro.
- `repro_stdout.log` and `repro_stderr.log`: captured output.

## Reproduction command

```bash
bash run_repro.sh
```
