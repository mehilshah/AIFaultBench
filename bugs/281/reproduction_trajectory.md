# Reproduction Trajectory — Bug 281: torch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10703](https://github.com/pyg-team/pytorch_geometric/issues/10703)
- **Repository:** pyg-team/pytorch_geometric @ `fae65964d712b1c93d620e23237a18b2f3ffaa9e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.12 virtual environment and install the dependencies from requirements.txt.
2. Run repro.py or bash run_repro.sh from the bug folder.
3. Observe the export failure in repro_stderr.log.

## Observed behavior

- With torch 2.8.0+cu128, torch-geometric 2.8.0, and pyg-lib 0.6.0+pt28cu126, torch.export.export() on a module calling torch_geometric.nn.knn_graph fails with torch._subclasses.fake_tensor.UnsupportedOperatorException: pyg.knn.default.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
