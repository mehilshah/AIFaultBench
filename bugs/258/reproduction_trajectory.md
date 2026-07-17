# Reproduction Trajectory — Bug 258: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2297](https://github.com/sdv-dev/SDV/issues/2297)
- **Repository:** sdv-dev/SDV @ `39f060e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created metadata with only `id` and `credit_card_number` columns, matching the bug report.
2. Fit `GaussianCopulaSynthesizer` on a DataFrame with those columns and verified that fitting completed with `_model=None` and no processed columns.
3. Called `get_learned_distributions()` and observed the `AttributeError` crash.

## Observed behavior

- run_repro.sh exited with status 1. stdout shows `after_fit _fitted=True _model=None` and `processed_columns=[]`. stderr shows `AttributeError: 'NoneType' object has no attribute 'to_dict'` from `sdv/single_table/copulas.py:221` when calling `get_learned_distributions()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
