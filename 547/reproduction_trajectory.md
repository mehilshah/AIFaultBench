# Reproduction Trajectory — Bug 547: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7733](https://github.com/deepspeedai/DeepSpeed/issues/7733)
- **Repository:** microsoft/DeepSpeed @ `5373a88000d8017e269277662cd8e93a814c66e1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean CPU-only venv and install requirements from requirements.txt.
2. Load codebase/deepspeed/runtime/data_pipeline/data_sampling/variable_batch_size_and_lr.py with minimal import stubs for unrelated DeepSpeed modules.
3. Call scale_lr(2, 4, 1.0, "sqrt") and observe the TypeError from torch.sqrt on a Python float.

## Observed behavior

- Running run_repro.sh loads codebase/deepspeed/runtime/data_pipeline/data_sampling/variable_batch_size_and_lr.py and fails with TypeError: sqrt(): argument 'input' (position 1) must be Tensor, not float when calling scale_lr(2, 4, 1.0, 'sqrt').

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
