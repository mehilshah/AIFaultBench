# Reproduction Trajectory — Bug 192: anomalib

- **Bug report:** [https://github.com/open-edge-platform/anomalib/issues/2929](https://github.com/open-edge-platform/anomalib/issues/2929)
- **Repository:** open-edge-platform/anomalib @ `c43e552`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read `bug_report.txt` and the Real-IAD source in `codebase/src/anomalib/data/datasets/image/realiad.py`.
2. Extracted the `CATEGORIES` tuple from the source file.
3. Compared it to the Real-IAD category list quoted in the report.
4. Observed a mismatch and a non-zero exit from `bash run_repro.sh`.

## Observed behavior

- Running `bash run_repro.sh` prints the hard-coded Real-IAD categories from `codebase/src/anomalib/data/datasets/image/realiad.py` and shows they do not match the 30-category list quoted in `bug_report.txt`. The script exits with status 1 and the log reports 20 missing categories and 20 extra categories.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
