# Reproduction Trajectory — Bug 475: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2768](https://github.com/sdv-dev/SDV/issues/2768)
- **Repository:** sdv-dev/SDV @ `ad8e4e09bdd01338ea94a60cddd1f06c815273aa`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Metadata object with two tables, add an 'address' column relationship to table.
2. Instantiate HMASynthesizer(metadata_example, locales=['en_US']).
3. Call synthesizer.add_constraints([FixedCombinations(table_name='table', column_names=['code', 'description'])]).
4. Observe the AttributeError when DataProcessor inspects the rebuilt SingleTableMetadata.

## Observed behavior

- Running the local repro prints the expected traceback: HMASynthesizer.add_constraints -> DataProcessor._detect_multi_column_transformers -> AttributeError: 'SingleTableMetadata' object has no attribute '_valid_column_relationships'. The original metadata instance does have _valid_column_relationships before the synthesizer rebuilds table metadata.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
