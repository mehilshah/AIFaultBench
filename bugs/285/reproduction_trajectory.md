# Reproduction Trajectory — Bug 285: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21804](https://github.com/Lightning-AI/pytorch-lightning/issues/21804)
- **Repository:** Lightning-AI/pytorch-lightning @ `4819088b0c6838f0d878b30050d59003305924b8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a venv with system site packages and install the Lightning runtime deps from `requirements.txt`.
2. Run `repro.py` with `PYTHONPATH=codebase/src` so the local source checkout is imported.
3. Observe the process crash during `fabric.save(...)` while using `FSDPStrategySubclass(state_dict_type='full')` on CPU with `devices=2`.

## Observed behavior

- Running `PYTHONPATH=codebase/src .venv/bin/python -u repro.py` in the local checkout spawned two CPU FSDP workers, printed the checkpoint save attempt on both ranks, and then terminated with `Segmentation fault (core dumped)` (exit code 139). `repro_stderr.log` also shows the peer-reset error that follows the worker crash.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
