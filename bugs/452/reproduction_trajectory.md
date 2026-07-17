# Reproduction Trajectory — Bug 452: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1400](https://github.com/huggingface/accelerate/issues/1400)
- **Repository:** huggingface/accelerate @ `fafadc532351f3434f4d4abd4b61d356932607d8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean venv and installed CPU `torch==2.3.1` plus the editable local `accelerate` source tree.
2. Ran a minimal iterable-dataset repro that exercises `accelerate.data_loader.DataLoaderDispatcher`'s batch slicing logic for 4 processes.
3. Observed that a single sample expands to a 2-row batch and is then sliced into empty tensors on ranks 2 and 3.

## Observed behavior

- Running `bash run_repro.sh` printed `observed_batch_size=1`, `batch_size_per_rank=1`, then `rank=2 input_ids_shape=(0, 3)` and `rank=3 input_ids_shape=(0, 3)`, followed by `BUG_REPRODUCED: ranks 2 and 3 receive empty tensors`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
