# Reproduction Trajectory — Bug 012: models

- **Bug report:** [https://github.com/tensorflow/models/issues/11112](https://github.com/tensorflow/models/issues/11112)
- **Repository:** tensorflow/models @ `325e10e2602e23c8a2d33a611c6b3286372b0b1a`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a fresh virtual environment with `python3 -m venv .venv`.
2. Installed `tensorflow==2.16.2` and `tf-keras==2.16.0` from `requirements.txt`.
3. Ran `python repro.py` through `run_repro.sh` and confirmed the import path did not raise the reported AttributeError.

## Observed behavior

- bash run_repro.sh completed successfully in a clean venv.
- The probe printed `tf_keras.optimizers.legacy.Optimizer present: True` and `ema_optimizer_imported_successfully`.
- A dry-run install of `tf-nightly-cpu==2.16.0.dev20231103` failed because that exact wheel is not available for this Python 3.12 build.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The exact TensorFlow nightly from the issue report cannot be installed in this environment, and the closest installable stable wheel set keeps `tf_keras.optimizers.legacy.Optimizer` present.
