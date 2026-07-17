# Bug 414 Repro

This bundle targets TorchRL issue https://github.com/pytorch/rl/issues/3550.

## Result

Not reproducible on this host.

Reason:
- The issue is MPS-specific.
- This machine is Linux, so Apple MPS is unavailable.
- The pinned TorchRL commit already contains the MPS float64 downcast fix.

## Files

- `repro.py`: guarded repro entrypoint.
- `requirements.txt`: minimal dependency set for the pinned TorchRL checkout.
- `setup_env.sh`: creates a virtual environment and installs dependencies.
- `run_repro.sh`: runs the repro.
- `reproduction.json`: schema-constrained result.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

On macOS with MPS available, `repro.py` exercises:
- `Unbounded(...).to("mps")`
- `SerialEnv(..., device="mps")` with a float64-observation sub-environment
