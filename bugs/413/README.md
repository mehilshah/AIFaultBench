# Bug 413

Detectron2 `Instances.__getitem__` fails when integer indexing produces a 0-d tensor field.

Files in this bundle:
- `bug_report.txt`: recovered issue report
- `codebase/`: Detectron2 source at `2612e4a90e77ce3ea650546ac99a91e8c6ac9aad`
- `repro.py`: minimal direct repro
- `setup_env.sh`: creates a local venv and installs dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `requirements.txt`: Python dependencies for the repro
- `reproduction.json`: final structured result

Run locally:
```bash
bash setup_env.sh
bash run_repro.sh
```
