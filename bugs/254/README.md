# Bug 254 Reproduction

This bundle reproduces the TorchTitan dataloader bug where `DataloaderStopIteration`
inherits from `StopIteration`, which turns the intended exception into:

`RuntimeError: generator raised StopIteration`

## Files

- `repro.py`: loads the real `codebase/torchtitan/components/dataloader.py` source file and triggers the failure path.
- `run_repro.sh`: runs the repro in the local venv.
- `setup_env.sh`: creates the isolated venv.
- `requirements.txt`: intentionally empty because the repro uses stdlib-only stubs.

## Run

```sh
sh setup_env.sh
sh run_repro.sh
```

The repro is expected to print `RuntimeError: generator raised StopIteration`.
