# Reproduction Trajectory — Bug 004: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/13490](https://github.com/tensorflow/models/issues/13490)
- **Repository:** tensorflow/models @ `8c5c79c27c4bb2843308bf8623daa24f4f3cbe62`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read bug_report.txt and located the target implementation in codebase/official/vision/ops/augment.py.
2. Created a self-checking repro script and supporting environment files.
3. Ran ./run_repro.sh and captured the output in repro_stdout.log and repro_stderr.log.

## Observed behavior

- Local source check found the buggy lines in codebase/official/vision/ops/augment.py.
- For alpha=0.2 and 100000 samples, the buggy sampler had variance 0.08315563201904297, almost identical to a uniform draw (0.08284700719769786) and far below the correct beta reference (0.1788089841121679).
- The buggy sampler's 10th/90th percentiles were 0.10028971955180169 and 0.899753749370575, while the correct beta reference was 0.00024746188615865826 and 0.999761842248624.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
