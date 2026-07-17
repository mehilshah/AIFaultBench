# Reproduction Trajectory — Bug 432: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10160](https://github.com/pyg-team/pytorch_geometric/issues/10160)
- **Repository:** pyg-team/pytorch_geometric @ `69193c895fe721fb45e63985bb79e8d130ee7782`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.9.25 virtual environment with uv.
2. Installed the pinned repro dependencies from `requirements.txt` (`pgmpy==1.0.0` and `pandas`).
3. Ran `python repro.py`, which imports `pgmpy.estimators.CITests.chi_square` and triggers the reported TypeError.

## Observed behavior

- On Python 3.9.25, `from pgmpy.estimators.CITests import chi_square` fails with `TypeError: unsupported operand type(s) for |: 'type' and 'type'` while importing `pgmpy/base/DAG.py` at the `weight: int | float = None` annotation. This is the same dependency path used by `torch_geometric.contrib.explain.PGMExplainer` in the local PyG codebase.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
