# Bug 531

This folder is a self-contained reproduction bundle for the RT-DETR `num_feature_levels > len(backbone outputs)` bug.

Files:
- `bug_report.txt`: recovered issue report
- `codebase/`: local transformers source used for reproduction
- `repro.py`: minimal script that triggers the failure and a control case
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: executes the repro and captures logs
- `manifest.json`: metadata for the standardized folder

Reproduction summary:
- `RTDetrForObjectDetection` with `num_feature_levels=4` raises `TypeError` in `RTDetrModel.forward`
- the same model with the default `num_feature_levels=3` path completes normally

Run:
```bash
./setup_env.sh
./run_repro.sh
```
