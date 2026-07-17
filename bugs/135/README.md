# Bug 135 Reproduction

This bundle checks the Docker Hub metadata for `google/deepvariant:1.6.1`.

Observed result on July 17, 2026:
- the image config reports `VERSION=1.6.0`
- the expected release version is `1.6.1`

That matches the bug report that the `1.6.1` image still prints `DeepVariant version 1.6.0`.

Files:
- `repro.py`: registry metadata check
- `run_repro.sh`: wrapper to run the repro
- `setup_env.sh`: no-op environment setup
- `requirements.txt`: empty dependency set because the repro uses the standard library only
- `manifest.json`: bundle metadata

Run locally:
```bash
bash run_repro.sh
```

Expected behavior:
- the script exits with status `1`
- stderr contains the VERSION mismatch
