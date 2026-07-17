# Reproduction Trajectory — Bug 015: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11058](https://github.com/tensorflow/models/issues/11058)
- **Repository:** tensorflow/models @ `9a2993d140841f37d73cded94c1295da4faab8b5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the `show_batch` cell from `codebase/docs/vision/instance_segmentation.ipynb`.
2. Inspect the function body and confirm `num_of_examples` is never read.
3. Execute `show_batch` with three records and `num_of_examples=1` in a stubbed environment.
4. Observe that the function still processes all three records.

## Observed behavior

- The notebook helper defines `show_batch(raw_records, num_of_examples)` but never references `num_of_examples`; when called with three records and `num_of_examples=1`, it still renders three subplots.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
