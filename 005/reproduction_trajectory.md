# Reproduction Trajectory — Bug 005: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11206](https://github.com/tensorflow/models/issues/11206)
- **Repository:** tensorflow/models @ `5445446014c80f23841afddbadf551d8c2adc200`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated environment with TensorFlow 2.16.1 and tf-keras 2.16.0.
2. Ran the import probe in repro.py.
3. Confirmed that tensorflow.python.framework.tensor is present and importable on this Linux/Python 3.12 host.

## Observed behavior

- The repro probe exited 0 on this host.
- stdout shows tensorflow=2.16.1, tf_keras=2.16.0, and tensorflow.python.framework.tensor resolves to site-packages/tensorflow/python/framework/tensor.py.
- The reported ImportError did not occur here; the import chain completed successfully.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported failure is not reproducible on this host. The issue appears to depend on a different platform or wheel combination than the one available here; the local Linux/Python 3.12 environment imports tf_keras successfully.
