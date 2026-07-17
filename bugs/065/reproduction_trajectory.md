# Reproduction Trajectory — Bug 065: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1194](https://github.com/keras-team/keras-io/issues/1194)
- **Repository:** keras-team/keras-io @ `af2817346c38effe497db8a771c5eb65f1e46144`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build the Docker image with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.

## Observed behavior

- Running `bash run_repro.sh` in a Python 3.10 container with `tensorflow==2.11.0` and `numpy<2` exits with code 1 after `ImportError: cannot import name 'FeatureSpace' from 'keras.utils' (/usr/local/lib/python3.10/site-packages/keras/utils/__init__.py)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
