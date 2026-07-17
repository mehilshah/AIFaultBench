# Reproduction Trajectory — Bug 510: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2739](https://github.com/sdv-dev/SDV/issues/2739)
- **Repository:** sdv-dev/SDV @ `7a3a902519afb8b8d1182bee2395a26b5cfe812d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Metadata object from the issue's multitable metadata snippet.
2. Fit HMASynthesizer on the provided main table with verbose disabled.
3. Sampled one row and counted the missing-datetime_format warnings emitted during fit/sample.

## Observed behavior

- Running HMASynthesizer on the bug report data captured 3 UserWarnings with the same missing-datetime_format message for main.denormalized_column.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
