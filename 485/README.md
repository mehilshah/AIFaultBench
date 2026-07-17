# Bug 485

Repro bundle for Lightning issue [#21567](https://github.com/Lightning-AI/pytorch-lightning/issues/21567).

## What this exercises

- `lightning_fabric.Fabric` with DDP and gradient accumulation
- `pytorch_lightning.demos.boring_classes.BoringModel`
- `warnings.filterwarnings(message=".*AccumulateGrad.*", action="error")`

## Files

- `repro.py`: minimal reproduction script
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: creates `.venv` and installs dependencies plus the local codebase
- `run_repro.sh`: activates the venv and runs the repro
- `reproduction.json`: schema-constrained result written after execution

## Notes

- The original report needs CUDA DDP. This host currently exposes a single GPU, so the bundle uses `devices=1` here and would use `devices=2` on a multi-GPU host.
- This host needs a PyTorch wheel that supports Blackwell (`sm_120`); the verified setup uses `torch==2.13.0+cu129`.
