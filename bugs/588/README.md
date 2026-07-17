# Bug 588 Reproduction

This folder reproduces the behavior reported in timm issue `#2453`.

What reproduces:
- Passing `pretrained_cfg_overlay='file=./pytorch_model.bin'` to `timm.create_model(...)` raises `TypeError: dataclasses.replace() argument after ** must be a mapping, not str`.

What does not fail:
- Using a proper mapping for `pretrained_cfg_overlay` works.
- Reusing the first three MobileNetV4 blocks as a backbone works.

Files:
- `repro.py`: standalone reproduction script
- `requirements.txt`: environment dependencies
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro script
- `reproduction.json`: schema-constrained result from the run
- `repro_stdout.log`, `repro_stderr.log`: captured command output

Reproduction command:
```bash
./run_repro.sh
```
