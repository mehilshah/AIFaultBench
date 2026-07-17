# Reproduction Trajectory — Bug 327: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2855](https://github.com/sdv-dev/SDV/issues/2855)
- **Repository:** sdv-dev/SDV @ `5b85738576fc67e7be37d66328dab839841db3ff`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local virtual environment and install dependencies with bash setup_env.sh.
2. Run the repro with bash run_repro.sh.
3. Inspect repro_stdout.log and repro_stderr.log for the diagnostic score and generated datetime ranges.

## Observed behavior

- Using sdv 1.35.1.dev0, the repro sampled datetime2 values outside the real data range (real: 2020-01-01 only; synthetic: 2019-07-04 09:28:36.084043560 to 2019-12-31 00:17:55.517074492) and run_diagnostic returned 0.75 with Data Validity 0.5.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
