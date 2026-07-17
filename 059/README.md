# Bug 059

This folder contains a minimal reproduction for
https://github.com/keras-team/keras-io/issues/1593.

Observed failure
- `keras_cv.metrics.BoxCOCOMetrics.result(force=True)` raises
  `InvalidArgumentError: ConcatOp : Dimension 1 in both shapes must be equal`
  when ground-truth boxes from successive updates have different per-image box counts.

Repro stack
- `tensorflow==2.19.1`
- `keras-cv==0.9.0`
- `pycocotools==2.0.11`

Files
- `repro.py`: minimal synthetic trigger
- `requirements.txt`: pinned runtime dependencies
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro script
- `reproduction.json`: schema-constrained outcome
- `repro_stdout.log` / `repro_stderr.log`: captured run output

Run
```bash
bash setup_env.sh
bash run_repro.sh
```
