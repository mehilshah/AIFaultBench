# Reproduction Bundle

This bundle reproduces the Object Detection import failure reported in `bug_report.txt`.

## What fails

Importing `object_detection.core.freezable_sync_batch_norm` reaches:

`tf.keras.layers.experimental.SyncBatchNormalization`

In TensorFlow 2.18, `tf.keras.layers.experimental` is no longer present, so the import raises:

`AttributeError: module 'keras._tf_keras.keras.layers' has no attribute 'experimental'`

## Files

- `repro.py`: minimal import harness
- `requirements.txt`: pinned TensorFlow version
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `manifest.json`: metadata for the bundle

## Run

```bash
bash run_repro.sh
```

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`
