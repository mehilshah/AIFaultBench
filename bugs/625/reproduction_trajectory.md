# Reproduction Trajectory — Bug 625: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7708](https://github.com/deepspeedai/DeepSpeed/issues/7708)
- **Repository:** microsoft/DeepSpeed @ `7f2f423257592725259a0950094dc9fe9d276a27`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local venv with the CPU PyTorch wheel and the small dependency set needed to import the local DeepSpeed source.
2. Ran repro.py, which triggers the real DeepSpeed backward hook path with grad=None.
3. Observed the TypeError in DeepSpeedEngine._backward_prologue_per_tensor when the hook tries to divide None by the gradient accumulation steps.

## Observed behavior

- Running ./run_repro.sh raises TypeError: unsupported operand type(s) for /: 'NoneType' and 'int' from DeepSpeedEngine._backward_prologue_per_tensor at codebase/deepspeed/runtime/engine.py:2335, reached through OutputBackwardHookManager.backward_hook in codebase/deepspeed/runtime/utils.py:1271.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
