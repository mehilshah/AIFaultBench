# Reproduction Trajectory — Bug 576: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3247](https://github.com/pytorch/rl/issues/3247)
- **Repository:** pytorch/rl @ `7e0968aa621c0b67313b3f5db09d931baf8a1b3b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated Python 3.12 venv and install CPU PyTorch 2.7.1 plus the minimal TorchRL dependencies from requirements.txt.
2. Run `./run_repro.sh` from the standardized bug folder with `codebase/` on `PYTHONPATH`.
3. Observe the AttributeError when `ReplayBuffer.register_save_hook(TED2Flat())` reaches `LazyMemmapStorage.register_save_hook`.

## Observed behavior

- Running `./run_repro.sh` in a clean venv prints `torch=2.7.1+cpu` and `storage=LazyMemmapStorage`, then fails with `AttributeError: 'LazyMemmapStorage' object has no attribute 'register_save_hook'` from `ReplayBuffer.register_save_hook` delegating to `self._storage.register_save_hook(hook)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
