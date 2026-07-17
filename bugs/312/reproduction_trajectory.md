# Reproduction Trajectory — Bug 312: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/82](https://github.com/PythonOT/POT/issues/82)
- **Repository:** PythonOT/POT @ `c5108efc7b6702e1af3928bef1032e6b37734d1c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install the bundle dependencies.
2. Install the local POT codebase in editable mode with the compatibility shims enabled by repro.py.
3. Run ot.gromov.gromov_wasserstein on dists0.txt and dists1.txt from the original notebook export.

## Observed behavior

- Running the bundled repro loads the original distance matrices, succeeds for the same-matrix call, and then fails on the slightly different matrices with TypeError: unsupported operand type(s) for *: 'NoneType' and 'float' at codebase/ot/optim.py:182.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
