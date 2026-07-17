# Reproduction Trajectory — Bug 461: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2799](https://github.com/sdv-dev/SDV/issues/2799)
- **Repository:** sdv-dev/SDV @ `f56af722f248d77c7dc2aa0a6683169f41e596b2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python environment with the pinned repro requirements.
2. Run `bash run_repro.sh`.
3. Observe that `Metadata().detect_from_dataframes(..., foreign_key_inference_algorithm='column_name_match')` returns `relationships: []` instead of the expected parent/child email relationship.

## Observed behavior

- The repro prints `Actual relationships: []` for a dataset where the child email values are a subset of the parent email key, then raises `AssertionError: semantic foreign key was not detected`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
