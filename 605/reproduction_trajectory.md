# Reproduction Trajectory — Bug 605: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2703](https://github.com/sdv-dev/SDV/issues/2703)
- **Repository:** sdv-dev/SDV @ `049106473fd32f00d2b551ef61864801792acc2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a multi-table Metadata object with district/account tables and one relationship.
2. Built a valid DayZ parameter dictionary and removed relationships for the single-table path.
3. Called SingleTableDayZSynthesizer.validate_parameters(metadata, parameters) and observed no exception.
4. Set relationships to ['a', 'b', 'c'] and called MultiTableDayZSynthesizer.validate_parameters(metadata, parameters), observing AttributeError.
5. Set min_cardinality to 0 and verified the multi-table validator accepted it.

## Observed behavior

- Single-table DayZ validation returned no exception for multi-table metadata when the relationships key was removed.
- Multi-table DayZ validation raised AttributeError ('str' object has no attribute 'keys') for relationships=['a', 'b', 'c'] instead of a structured validation error.
- min_cardinality=0 validated successfully.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
