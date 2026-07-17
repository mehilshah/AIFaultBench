# Reproduction Trajectory — Bug 446: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2803](https://github.com/sdv-dev/SDV/issues/2803)
- **Repository:** sdv-dev/SDV @ `74744e5f87fa72bdff14d031eafeaa21a4085088`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install `sdv==1.33.1` from `requirements.txt`.
2. Download `download_demo(modality='multi_table', dataset_name='financial')`.
3. Compare each table's dataframe column order against `metadata.to_dict()['tables'][table]['columns'].keys()`.

## Observed behavior

- Running `bash run_repro.sh` against `sdv==1.33.1` printed `same_order=True` for every table in the `financial` demo dataset and ended with `BUG_NOT_REPRODUCED`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The `financial` demo metadata currently matches the actual table column order for every table checked, so the mismatch described in the issue is not present in this environment.
