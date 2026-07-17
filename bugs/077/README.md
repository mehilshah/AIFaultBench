# Bug 077 Repro Bundle

This folder contains a self-contained reproduction bundle for:
`https://github.com/matterport/Mask_RCNN/issues/2979`

The issue report shows a TensorFlow `NotFoundError` during `model.fit()`.
The real failure is a missing image path consumed by the input pipeline, not
TensorBoard itself.

## What the repro does

`repro.py`:
- loads one real JPEG from `codebase/images/`
- injects one missing JPEG path
- builds a tiny Keras model
- calls `model.fit()` with a `TensorBoard` callback

The dataset fails when TensorFlow reaches `tf.io.read_file()` for the missing
path, which reproduces the reported `ReadFile`/`IteratorGetNext` failure mode.

## Run it

```bash
./setup_env.sh
./run_repro.sh
cat reproduction.json
```

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: runtime dependency pin
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: executes the reproducer and captures logs
- `repro_stdout.log` / `repro_stderr.log`: captured run output

