# Reproduction Trajectory — Bug 227: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/229](https://github.com/PythonOT/POT/issues/229)
- **Repository:** PythonOT/POT @ `f613942`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment and installed the bug-specific dependencies from requirements.txt.
2. Installed the local codebase in editable mode with build isolation disabled so the bundled Cython extension could compile.
3. Ran the exact issue matrix through ot.emd after adding a NumPy legacy alias for np.int required by POT 0.7.0 on modern NumPy.
4. Verified that the returned plan is feasible but has much higher cost than the manual reference plan Q.

## Observed behavior

- With NumPy 1.26.4 and SciPy 1.11.4, the local POT 0.7.0 codebase reproduces the reported behavior: ot.emd returns a feasible transport plan P with exact row/column sums, but P has cost 354.43787279000003 while the manual plan Q from the report has cost 57.54321038317501.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
