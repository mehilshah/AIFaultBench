# Reproduction Trajectory — Bug 553: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2716](https://github.com/sdv-dev/SDV/issues/2716)
- **Repository:** sdv-dev/SDV @ `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal Metadata object with one table.
2. Patched HMASynthesizer._estimate_num_columns to return a huge value and _get_distributions to avoid unrelated setup.
3. Instantiated HMASynthesizer and captured the PerformanceAlert output.

## Observed behavior

- HMASynthesizer printed an uncapped column count: (1000000000000000000000000000000 columns) instead of the requested (1000000+ columns) cap.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
