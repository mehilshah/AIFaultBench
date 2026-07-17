# Reproduction Trajectory — Bug 631: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2701](https://github.com/sdv-dev/SDV/issues/2701)
- **Repository:** sdv-dev/SDV @ `049106473fd32f00d2b551ef61864801792acc2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the local SDV checkout from ./codebase with pip.
2. Run repro.py to create DayZ parameters and change DAYZ_SPEC_VERSION to V1000.
3. Call DayZSynthesizer.validate_parameters(metadata, dayz_parameters).

## Observed behavior

- bash run_repro.sh printed `NO_ERROR` and then `V1000`, showing that `DayZSynthesizer.validate_parameters(metadata, dayz_parameters)` accepted an invalid DAYZ_SPEC_VERSION instead of raising.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
