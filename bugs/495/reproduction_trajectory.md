# Reproduction Trajectory — Bug 495: torch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10024](https://github.com/pyg-team/pytorch_geometric/issues/10024)
- **Repository:** pyg-team/pytorch_geometric @ `bfbe99faac5f8eaed689bde7683a377594cf4023`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtual environment with CUDA-enabled torch 2.11.0+cu128 and install the local codebase editable.
2. Run a minimal graph model on cuda and instantiate PGExplainer without moving the explainer to cuda.
3. Call PGExplainer.train(); the internal MLP remains on cpu and F.linear raises the reported device-mismatch RuntimeError.

## Observed behavior

- repro.py prints model_device=cuda:0, input_device=cuda:0, and explainer_mlp_device=cpu before training.
- run_repro.sh fails in codebase/torch_geometric/explain/algorithm/pg_explainer.py:130 with RuntimeError: Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
