# Reproduction Trajectory — Bug 069: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1489](https://github.com/keras-team/keras-io/issues/1489)
- **Repository:** keras-team/keras-io @ `88f51034b4e9f473e5d45247fc06fdc95108f7ec`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a synthetic DataFrame that matches the example's `Date Time` string column and numeric weather columns.
2. Called the example's `show_heatmap` logic with `plt.matshow(data.corr())`.
3. Observed the same ValueError reported in the issue.

## Observed behavior

- Running the repro in a local virtualenv prints pandas 3.0.3, then fails in `show_heatmap(df)` at `plt.matshow(data.corr())` with `ValueError: could not convert string to float: '01.01.2009 00:10:00'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
