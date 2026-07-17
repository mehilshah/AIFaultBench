# Reproduction Trajectory — Bug 437: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1419](https://github.com/huggingface/accelerate/issues/1419)
- **Repository:** huggingface/accelerate @ `ab379793d44be16d8fcac5c098a3ab9b6f5a7ec3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python environment with the bug-specific dependencies and installed the pinned local accelerate checkout.
2. Ran a minimal Accelerate training/eval loop that logs train metrics with step=completed_steps and eval metrics with a separate step counter that regresses relative to W&B's current step.
3. Observed W&B drop the eval logs for steps 1 and 2 while accepting the train logs and the final epoch summary.

## Observed behavior

- run_repro.sh completed successfully after recreating a clean venv from setup_env.sh.
- repro_stderr.log contains W&B warnings: 'Step only supports monotonically increasing values' and 'User provided step: 1 is less than current step: 3. Dropping entry ...' for batch_eval_loss.
- The offline W&B run history only retains the train-side metrics and drops the out-of-order eval-side entries.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
