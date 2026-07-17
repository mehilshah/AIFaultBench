# Reproduction Trajectory — Bug 205: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/229](https://github.com/PythonOT/POT/issues/229)
- **Repository:** PythonOT/POT @ `f613942`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Patched NumPy/SciPy runtime compatibility in the repro harness so the legacy POT code imports on the host Python 3.12 environment.
2. Ran `ot.emd` on the issue's 5x5 cost matrix and verified the returned transport plan satisfies the marginals.
3. Compared the returned cost against the manual plan from the bug report and confirmed the returned plan is much worse, reproducing the bug.

## Observed behavior

- Running `bash run_repro.sh` on the local codebase prints POT 0.7.0, returns a feasible plan with exact marginals, and shows `P cost: 354.43787279000003` versus the manual reference `Q cost: 57.54321038317501`. The script then fails with `AssertionError: BUG REPRODUCED: ot.emd returned a feasible but suboptimal plan`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
