# Bug 403 Repro Bundle

Issue: https://github.com/pyg-team/pytorch_geometric/issues/10276

## What this reproduces

The report uses `lightning_fabric.Fabric(devices=[0, 1], strategy="ddp")` with a `GConvGRU` layer built on `torch_geometric.nn.ChebConv`.

## Files

- `repro.py`: faithful reproduction script from the issue body
- `gconv_gru.py`: vendored upstream `GConvGRU` helper used by the report
- `requirements.txt`: Python dependencies inferred from the report
- `setup_env.sh`: environment bootstrap for CUDA 12.1 / PyTorch 2.5.1
- `run_repro.sh`: launcher for the repro script

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

## Notes

- This host currently exposes only one CUDA device, so the reported 2-GPU DDP path cannot be exercised here.
- The local base Python environment also has a broken `torch` install, so the final result is marked blocked rather than reproducible on this machine.
