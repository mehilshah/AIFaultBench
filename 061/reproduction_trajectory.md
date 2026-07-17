# Reproduction Trajectory — Bug 061: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1555](https://github.com/keras-team/keras-io/issues/1555)
- **Repository:** keras-team/keras-io @ `fc340b9989cdf17fba44e66efa22758afad39b87`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv with ./setup_env.sh.
2. Run ./run_repro.sh to load keras_cv/models/weights.py directly.
3. Observe the ImportError raised from from keras.utils import data_utils.

## Observed behavior

- Running ./run_repro.sh installs tensorflow==2.16.1, keras==3.0.5, and keras-cv==0.4.0, then loads .venv/lib/python3.11/site-packages/keras_cv/models/weights.py. The load fails with ImportError: cannot import name 'data_utils' from 'keras.utils' (.venv/lib/python3.11/site-packages/keras/utils/__init__.py).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
