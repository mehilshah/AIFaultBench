# Bug 462 Reproduction

This folder reproduces PyG issue 10138 on the pinned `torch_geometric` commit.

Files:
- `repro.py`: minimal crash reproducer
- `requirements.txt`: runtime dependency pinning
- `setup_env.sh`: creates a clean virtualenv and installs dependencies
- `run_repro.sh`: activates the environment and runs the reproducer
- `manifest.json`: standardized metadata

Reproduction command:
```bash
bash setup_env.sh && bash run_repro.sh
```
