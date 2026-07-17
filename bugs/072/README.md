# Bug 072 Reproduction

This folder reproduces the `AttributeError` reported in DeepSpeedExamples issue 924.

## What fails

The failing call site is:

- [`codebase/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/main.py:367`](codebase/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/main.py#L367)

That line passes `model.model` into `print_throughput(...)`, but a `DeepSpeedEngine` exposes the wrapped model as `module`, not `model`.

## How to run

```bash
bash run_repro.sh
```

The repro is intentionally minimal and does not need the full training stack.

