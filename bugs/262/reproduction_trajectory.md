# Reproduction Trajectory — Bug 262: tensorly

- **Bug report:** [https://github.com/tensorly/tensorly/issues/607](https://github.com/tensorly/tensorly/issues/607)
- **Repository:** tensorly/tensorly @ `3912bb9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create an isolated Python 3.12 virtual environment.
2. Install NumPy 2.3.1, SciPy, and the local TensorLy codebase in editable mode.
3. Run the complex-valued Tensor Train rank sweep from the bug report on a fixed random seed.
4. Observe that the reconstruction MSE increases overall as rank grows.

## Observed behavior

- In a fresh venv with NumPy 2.3.1, SciPy 1.18.0, and local TensorLy 0.9.0, the complex TT rank sweep prints [1.972 2.018 2.028 2.057 2.085 2.122 2.156 2.234 2.297 2.401 2.387 2.378 2.433 2.587], and the last value is larger than the first, so the error is not monotonically decreasing with rank.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
