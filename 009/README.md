# Bug 009 Repro Bundle

This folder contains a standalone repro bundle for TensorFlow Models issue
11133.

## What I checked

The local `research/object_detection/exporter_lib_v2.py` defines
`DetectionFromImageModule` as a `tf.Module`, and the checked-in exporter entry
point `research/object_detection/exporter_main_v2.py` delegates to it without a
direct `.outputs` access. In this workspace TensorFlow is not installed, so the
runtime export path cannot be executed here.

## Files

- `repro.py`: source-aware repro helper.
- `requirements.txt`: dependency list for the repro environment.
- `setup_env.sh`: installs the dependencies.
- `run_repro.sh`: runs the repro and captures logs.
- `reproduction.json`: schema-constrained verdict.

## Reproduction command

```bash
bash run_repro.sh
```
