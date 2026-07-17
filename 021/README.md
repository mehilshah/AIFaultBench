# Bug 021

This folder contains a self-contained reproduction for the Model Garden
`ConcatV2` failure reported in `official/vision/modeling/layers/detection_generator.py`.

Trigger:
- `MultilevelDetectionGenerator` in `nms_version="v2"` class-aware mode
- raw scores with only the implicit background channel
- after background slicing, the class dimension becomes zero
- `_generate_detections_v2_class_aware()` reaches `tf.concat([])` and raises
  `InvalidArgumentError` from `ConcatV2`

Files:
- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependency pin
- `setup_env.sh`: local venv bootstrap
- `run_repro.sh`: executes the repro and writes logs
- `reproduction.json`: machine-readable outcome
- `repro_stdout.log` / `repro_stderr.log`: captured run output

Run:
```bash
bash run_repro.sh
```
