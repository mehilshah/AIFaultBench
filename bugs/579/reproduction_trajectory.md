# Reproduction Trajectory — Bug 579: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2711](https://github.com/sdv-dev/SDV/issues/2711)
- **Repository:** sdv-dev/SDV @ `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an object-dtype Series containing numeric data and a null value.
2. Run the same fillna logic used by `HMASynthesizer._clear_nans` in `codebase/sdv/multi_table/hma.py`.
3. Capture warnings and confirm pandas emits one FutureWarning with the downcasting message.

## Observed behavior

- Using pandas 2.2.3, the HMA `_clear_nans` fillna branch emits the expected FutureWarning: "Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version..."

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
