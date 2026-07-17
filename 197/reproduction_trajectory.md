# Reproduction Trajectory — Bug 197: MONAI

- **Bug report:** [https://github.com/Project-MONAI/MONAI/issues/8602](https://github.com/Project-MONAI/MONAI/issues/8602)
- **Repository:** Project-MONAI/MONAI @ `69f3dd2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtualenv with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Inspect `repro_stdout.log` for the swapped output shapes.

## Observed behavior

- Running `bash run_repro.sh` produces `buffer_shape=(12, 5)`, `mean_batch_shape=(5,)`, and `mean_channel_shape=(12,)` in `repro_stdout.log`.
- The repro script reports `shape_mismatch=expected mean_batch=(3,), mean_channel=(5,); got mean_batch=(5,), mean_channel=(12,)` and exits with status 1.
- The implementation in `codebase/monai/metrics/utils.py` reduces `mean_batch` with `sum(dim=0)` and `mean_channel` with `sum(dim=1)`, which matches the swapped behavior from the report.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
