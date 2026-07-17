# Bug 012

TensorFlow Models issue: `https://github.com/tensorflow/models/issues/11112`

This bundle probes the import path around
`official/modeling/optimization/ema_optimizer.py`, which is where the reported
`tf_keras.optimizers.legacy.Optimizer` attribute error would surface.

Files in this folder:
- `bug_report.txt`: original report text
- `codebase/`: local TensorFlow Models snapshot
- `repro.py`: minimal import probe
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: executes the repro inside that virtualenv
- `manifest.json`: bundle metadata
- `reproduction.json`: final reproducibility result
- `repro_stdout.log` and `repro_stderr.log`: run output

Observed here:
- `tf_keras.optimizers.legacy.Optimizer` is present in the installable wheels
- importing `ema_optimizer.py` succeeds with the available wheels
- the exact `tf-nightly-cpu==2.16.0.dev20231103` package from the report is not available for this Python build, so the historical crash could not be reproduced locally
