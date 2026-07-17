# Reproduction Trajectory — Bug 519: torch-geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10018](https://github.com/pyg-team/pytorch_geometric/issues/10018)
- **Repository:** pyg-team/pytorch_geometric @ `1ab39939d3ef44afa816b1bec4a84c957ad990f2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create the isolated Python environment.
2. Run `bash run_repro.sh` to build the sandbox package tree and import `torch_geometric.graphgym.imports`.
3. Observe the ModuleNotFoundError for `torch_geometric.graphgym.imports` in the output logs.

## Observed behavior

- run_repro.sh prints `raised=ModuleNotFoundError` and `message=No module named 'torch_geometric.graphgym.imports'`.
- The isolated sandbox built by repro.py omits `torch_geometric/graphgym/imports.py` and triggers the same missing-module exception reported in the bug.
- repro_stdout.log contains the reproduced ModuleNotFoundError; repro_stderr.log is empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
