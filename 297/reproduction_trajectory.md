# Reproduction Trajectory — Bug 297: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10629](https://github.com/pyg-team/pytorch_geometric/issues/10629)
- **Repository:** pyg-team/pytorch_geometric @ `b783d593d4a63472a1f67d95855d54dcd75a74f8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Use the bundled pyproject.toml that mirrors the issue report's torch, torchvision, torch_geometric, and uv index configuration.
2. Run bash run_repro.sh from the bug folder.
3. Observe uv sync fail with an unsatisfiable dependency resolution for torch-geometric.

## Observed behavior

- Running bash run_repro.sh fails during uv dependency resolution with: 'torch-geometric was not found in the package registry' and a hint that https://data.pyg.org/whl/torch-2.8.0+cu128.html returned 403 Forbidden.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
