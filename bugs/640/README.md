# Bug 640 Reproduction Bundle

This folder contains a self-contained reproduction for the timm transform bug described in `bug_report.txt`.

Observed behavior:
- `create_transform(..., is_training=False, crop_pct=1)` still applies a center crop for non-square images.
- A feature placed near the left edge of a wide image is removed by the transform, even though the user expected a pure resize.

Files:
- `repro.py`: generates a synthetic image and measures the crop effect.
- `requirements.txt`: runtime dependencies for a clean repro environment.
- `setup_env.sh`: creates an isolated virtualenv and installs dependencies.
- `run_repro.sh`: runs the repro and captures logs.
- `manifest.json`: standardized metadata.
- `reproduction.json`: final verdict written after verification.
- `repro_stdout.log`, `repro_stderr.log`: captured command output.

Reproduction command:
`bash run_repro.sh`
