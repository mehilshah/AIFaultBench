# Reproduction Trajectory — Bug 618: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2702](https://github.com/sdv-dev/SDV/issues/2702)
- **Repository:** sdv-dev/SDV @ `049106473fd32f00d2b551ef61864801792acc2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local Python virtualenv with `bash setup_env.sh`.
2. Run `bash run_repro.sh` to exercise the reported empty-table case and the two all-null column cases.
3. Observe that each call to `DayZSynthesizer.create_parameters` raises instead of returning valid default parameters.
4. Confirm the failure messages in `repro_stdout.log`.

## Observed behavior

- In this checkout, `DayZSynthesizer.create_parameters` does not fall back to defaults for the reported edge cases. The reported empty-table snippet raises `AttributeError: 'float' object has no attribute 'item'`. An all-null numerical column with explicit metadata raises the same `AttributeError`. An all-null datetime column with explicit metadata raises `ValueError: NaTType does not support strftime`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
