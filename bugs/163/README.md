# Reproduction Bundle

This bundle reproduces the YOLOV8 SavedModel export behavior described in
`bug_report.txt`.

Observed result:

- `YOLOV8Detector(image)["boxes"]` has shape `(1, 5376, 64)`.
- The SavedModel signature exported from the same model reports
  `outputs['boxes'] tensor_info` with shape `(-1, -1, 64)`.

Run:

```bash
bash setup_env.sh
bash run_repro.sh
```

The `run_repro.sh` script expects the local `codebase/` directory to remain in
place and uses it through `PYTHONPATH`.
