# Reproduction Trajectory — Bug 052: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1795](https://github.com/keras-team/keras-io/issues/1795)
- **Repository:** keras-team/keras-io @ `3648974a8a88221a4e3ec7edf59260908c06a353`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local virtualenv and installed the pinned repro stack from requirements.txt.
2. Ran run_repro.sh, which executed the minimal NER Transformer training loop on synthetic variable-length token/tag data.
3. Observed successful fit and predict output, including 'RESULT: success', instead of the reported softmax graph error.

## Observed behavior

- On TensorFlow 2.16.1 and Keras 3.1.0, the minimal NER model fit completed successfully and prediction also completed; no OperatorNotAllowedInGraphError or Softmax.call() failure occurred.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash ./run_repro.sh
```

## Why it does not reproduce on the reference machine

The exact issue-specific Keras dev build is not available on PyPI, and the closest installable stack (TensorFlow 2.16.1 + Keras 3.1.0) does not reproduce the bug here.
