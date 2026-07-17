# Reproduction Trajectory — Bug 057: keras

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1665](https://github.com/keras-team/keras-io/issues/1665)
- **Repository:** keras-team/keras-io @ `c03f5949ad10a2b008882fce2bb2d18c80f3e725`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.11 virtual environment
2. Install the pinned dependencies from requirements.txt
3. Run repro.py

## Observed behavior

- With TensorFlow 2.14.0, Keras 2.14.0, and numpy<2, running the repro hits ImportError: cannot import name 'ops' from 'keras'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
