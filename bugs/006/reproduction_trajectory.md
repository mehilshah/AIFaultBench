# Reproduction Trajectory — Bug 006: models

- **Bug report:** [https://github.com/tensorflow/models/issues/11134](https://github.com/tensorflow/models/issues/11134)
- **Repository:** tensorflow/models @ `e923b8aa3b066c02432ffdb7d5fd93d465b6eaa5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed the repro dependencies.
2. Built an EfficientNet-B1 feature slice from the local TensorFlow Models codebase.
3. Minimized a dummy loss over the full backbone variable list and observed the missing-gradient warning.

## Observed behavior

- Running `bash run_repro.sh` emitted `WARNING:absl:Gradients do not exist for variables [...] when minimizing the loss.` in `repro_stderr.log`, including EfficientNet-B1 layers such as `stack_6/block_1/...` and `top_bn/...`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
