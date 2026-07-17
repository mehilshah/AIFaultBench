# Bug 349 Reproduction

Recovered from issue: https://github.com/huggingface/accelerate/issues/3140

## Summary

`Accelerator.save_state()` fails in the DeepSpeed branch when multiple models are present and one of them is frozen. The failure is caused by calling `save_checkpoint()` on every model in `self._models`, including a frozen DeepSpeed engine whose `checkpoint_engine` is `None`.

## Files

- `repro.py`: minimal driver that forces the DeepSpeed `save_state()` branch and reproduces the exception
- `requirements.txt`: minimal runtime dependency set for the repro environment
- `setup_env.sh`: creates a local virtualenv and installs the dependencies
- `run_repro.sh`: runs the repro inside the virtualenv
- `codebase/`: local Accelerate source snapshot used by the repro

## How to run

```bash
bash run_repro.sh
```

Expected failure:

```text
AttributeError: 'NoneType' object has no attribute 'makedirs'
```
