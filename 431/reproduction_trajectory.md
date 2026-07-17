# Reproduction Trajectory — Bug 431: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2813](https://github.com/sdv-dev/SDV/issues/2813)
- **Repository:** sdv-dev/SDV @ `7c574997e9027edce53820b5f38134fb3e5d05c0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded the 3-table metadata from the bug report.
2. Removed the foreign key column table2.fk_1.
3. Observed that both relationships were deleted instead of only the table2 relationship.

## Observed behavior

- Before removal, the metadata contained two relationships. After calling remove_column(table_name='table2', column_name='fk_1'), metadata.relationships became empty, and the repro script raised an AssertionError because the table1 -> table3 relationship should have remained.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
