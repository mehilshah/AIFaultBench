# Reproduction Trajectory — Bug 611: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/960](https://github.com/huggingface/accelerate/issues/960)
- **Repository:** huggingface/accelerate @ `30a6a3435fc49ee7185d5e14d2abff6854c48b4d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated venv and install the CPU torch wheel plus the local editable `accelerate` source.
2. Launch the repro under `accelerate.debug_launcher` with two CPU processes.
3. Run one train batch, then a full eval epoch, then resume training on the original train iterator.
4. Observe that `GradientState.end_of_dataloader` stays `True` after eval and `gather_for_metrics` truncates the following train batch.

## Observed behavior

- After the eval loop, `state_after_eval` was `Sync Gradients: True / At end of current dataloader: True / Extra samples added: 2`.
- The next train batch gathered with `gather_for_metrics` had shape `(2,)` and values `[4, 5]` even though the expected gathered size was `4`.
- The repro terminated with `AssertionError: gather_for_metrics truncated a non-final train batch after eval`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
