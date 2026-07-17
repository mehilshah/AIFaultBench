# Bug 495

Reproduction bundle for the PGExplainer device-mismatch bug from:
https://github.com/pyg-team/pytorch_geometric/issues/10024

Observed failure:
`RuntimeError: Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu`

Root cause in this snapshot:
`PGExplainer` creates its internal MLP on CPU unless the explainer itself is moved to CUDA before training.

Files:
- `repro.py`: minimal CUDA repro against the local `codebase/`
- `requirements.txt`: runtime dependencies
- `setup_env.sh`: creates a clean virtual environment and installs dependencies
- `run_repro.sh`: one-command launcher
- `manifest.json`: metadata for this standardized folder

Usage:
```bash
bash run_repro.sh
```
