# Reproduction Trajectory — Bug 349: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/3140](https://github.com/huggingface/accelerate/issues/3140)
- **Repository:** huggingface/accelerate @ `5060574827ffcf1055179896cbb4f150caa3aec5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv and install the minimal CPU torch + accelerate dependencies.
2. Run `bash run_repro.sh` with `PYTHONPATH` pointing at `codebase/src`.
3. Observe the traceback from `Accelerator.save_state()` when the frozen model is checkpointed.

## Observed behavior

- Running `bash run_repro.sh` reaches `Accelerator.save_state()` in `codebase/src/accelerate/accelerator.py:3039`.
- The second model's `save_checkpoint()` raises `AttributeError: 'NoneType' object has no attribute 'makedirs'`, matching the bug report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
