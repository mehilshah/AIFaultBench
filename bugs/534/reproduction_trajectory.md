# Reproduction Trajectory — Bug 534: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1163](https://github.com/huggingface/accelerate/issues/1163)
- **Repository:** huggingface/accelerate @ `3533e2b0b167238fcdd3c636dcf6c3c6de983efa`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh venv and installed torch 2.3.1+cpu plus the local editable accelerate codebase.
2. Ran repro.py to save 20 automatic checkpoints under a project configuration with total_limit=3.
3. Compared the final checkpoint folder names against the expected latest three numeric checkpoints.

## Observed behavior

- After 20 calls to Accelerator.save_state() with ProjectConfiguration(total_limit=3, automatic_checkpoint_naming=True), the final retained checkpoints were ['checkpoint_19', 'checkpoint_8', 'checkpoint_9'] instead of the expected latest three numeric checkpoints ['checkpoint_17', 'checkpoint_18', 'checkpoint_19'].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
