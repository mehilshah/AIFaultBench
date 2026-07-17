# Reproduction Trajectory — Bug 644: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2700](https://github.com/sdv-dev/SDV/issues/2700)
- **Repository:** sdv-dev/SDV @ `049106473fd32f00d2b551ef61864801792acc2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an empty `pandas.DataFrame()`.
2. Create an empty `sdv.metadata.Metadata()`.
3. Call `sdv.single_table.DayZSynthesizer.create_parameters(data, metadata)`.
4. Observe the `KeyError: None` traceback.

## Observed behavior

- Running `DayZSynthesizer.create_parameters(pd.DataFrame(), Metadata())` in the local codebase raises `KeyError: None`. The traceback points to `sdv/single_table/_dayz_utils.py:37` at `metadata.tables[table_name]` after `Metadata._get_single_table_name()` returns `None` for empty metadata.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
