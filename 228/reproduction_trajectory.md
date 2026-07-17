# Reproduction Trajectory — Bug 228: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/691](https://github.com/PythonOT/POT/issues/691)
- **Repository:** PythonOT/POT @ `68e3926`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python 3.11 virtual environment and installed numpy==1.26.4 and scipy==1.13.1.
2. Loaded the local POT source files from codebase/ without importing the package root.
3. Ran the exact sinkhorn_knopp_unbalanced example from bug_report.txt and observed the 0.9.5 matrix.

## Observed behavior

- In a clean Python 3.11 virtualenv with numpy==1.26.4 and scipy==1.13.1, the local source tree returned [[0.32205361, 0.1184769], [0.1184769, 0.32205361]] for the exact 2x2 example in bug_report.txt. That matches the POT 0.9.5 value from the report and differs from the POT 0.9.4 control value [[0.51122814, 0.18807032], [0.18807032, 0.51122814]].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
