# Reproduction Trajectory — Bug 037: labml-ai annotated deep learning paper implementations

- **Bug report:** [https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/251](https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/251)
- **Repository:** labmlai/annotated_deep_learning_paper_implementations @ `999f2036a5a7c54403352211b5d1cc0df42b83f6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Force the attention matrix to the identity so the value path is isolated.
2. Run the single-rotation reference path and the current double-rotation path on the same input.
3. Compare outputs: the reference matches the input, but the current code does not.

## Observed behavior

- With identity attention, the corrected path reconstructs the input (max_abs_diff(correct, input) = 1.7763568394e-15), while the current implementation returns a rotated tensor (max_abs_diff(buggy, input) = 20.8207225627).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
