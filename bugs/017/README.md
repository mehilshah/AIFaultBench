# Bug 017

This folder contains a self-contained repro bundle for the TensorFlow Models issue referenced in `bug_report.txt`.

## Result

The reported empty-tensor / `???` failure was **not reproducible** in this checkout.

Running `./setup_env.sh && ./run_repro.sh`:

- installs TensorFlow 2.21.0 in a local virtual environment
- loads the `ssd_mobilenet_v1_coco_2017_11_17` SavedModel
- runs inference on `codebase/research/object_detection/test_images/image1.jpg`
- prints non-empty detections with `num_detections=100` and a top score of `0.9406895041465759`

## Files

- `repro.py`: standalone inference repro
- `requirements.txt`: Python dependencies
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: executes the repro
- `reproduction.json`: machine-readable outcome
- `repro_stdout.log` / `repro_stderr.log`: captured command output
