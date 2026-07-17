# Reproduction Trajectory — Bug 632: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/9818](https://github.com/pyg-team/pytorch_geometric/issues/9818)
- **Repository:** pyg-team/pytorch_geometric @ `46705844b39ededc0fcef1de90e73923480a6446`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated virtual environment.
2. Installed torch==2.5.1+cpu plus the package's core Python dependencies.
3. Installed the local codebase in editable mode.
4. Constructed a small homogeneous Data graph and instantiated NeighborLoader with input_nodes=train_mask.
5. Iterated the loader to trigger NeighborSampler._sample(), which raised the ImportError.

## Observed behavior

- In a fresh venv with torch==2.5.1+cpu and the local torch-geometric checkout, the repro prints WITH_PYG_LIB=False and WITH_TORCH_SPARSE=False, then NeighborLoader() and fails with ImportError: 'NeighborSampler' requires either 'pyg-lib' or 'torch-sparse'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
