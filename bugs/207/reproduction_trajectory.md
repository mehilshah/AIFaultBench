# Reproduction Trajectory — Bug 207: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/712](https://github.com/PythonOT/POT/issues/712)
- **Repository:** PythonOT/POT @ `39cd6ec`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspected bug_report.txt and identified the reported ot.dist minkowski behavior.
2. Ran the report's 1D example against the local codebase and observed that p=1 and p=2 are identical in 1D, which is expected.
3. Ran a 2D control against the local codebase and verified that minkowski p is respected and matches SciPy.
4. Packaged the repro bundle and captured stdout/stderr in repro_stdout.log and repro_stderr.log.

## Observed behavior

- In the checked-out codebase (ot version 0.9.6dev0), the 1D report sample gives identical results for minkowski p=1 and p=2, but 1D Minkowski distance is mathematically identical for all p and therefore does not isolate the bug.
- A 2D control case shows ot.dist(..., metric="minkowski", p=1/2/3) differs across p values and matches scipy.spatial.distance.cdist exactly (max absolute error 0.0 for each p).
- The reproduction script exits successfully and prints a summary with reproducible=false.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The checked-out codebase does not reproduce the reported bug; the apparent issue is caused by using a 1D example where Minkowski distances are identical for all p.
