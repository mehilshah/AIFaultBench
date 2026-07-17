# Reproduction Trajectory — Bug 476: torch-geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10116](https://github.com/pyg-team/pytorch_geometric/issues/10116)
- **Repository:** pyg-team/pytorch_geometric @ `d2bb939a1bfba3b7a6f7d7b102a2771471657319`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- In a fresh venv with torch-geometric==2.6.1, repro.py prints has_HashTensor=False and then fails with ImportError: cannot import name 'HashTensor' from 'torch_geometric'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
