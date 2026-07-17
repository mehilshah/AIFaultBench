# Bug 610

This folder contains a self-contained repro bundle for Lightning issue `#21435`.

Observed result in this snapshot:
- `repro.py` raises the reported `RuntimeError`
- the local `lightning` snapshot is version `2.6.0`
- `MixedPrecision.clip_gradients()` still raises for optimizers that expose `_step_supports_amp_scaling`, even when `bf16-mixed` has no scaler

Files:
- `repro.py`: minimal runtime check for the reported AMP + fused AdamW clipping path
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates a clean virtual environment and installs dependencies
- `run_repro.sh`: runs the repro and captures stdout/stderr
- `manifest.json`: bundle metadata

Run:
```bash
bash run_repro.sh
```
