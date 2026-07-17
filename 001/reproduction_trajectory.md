# Reproduction Trajectory — Bug 001: models

- **Bug report:** [https://github.com/tensorflow/models/issues/166](https://github.com/tensorflow/models/issues/166)
- **Repository:** tensorflow/models @ `05630a7578b25390f469b2f91f2c2326e5ed539b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated Python environment and installed the repro dependencies from requirements.txt.
2. Executed repro.py through run_repro.sh.
3. Observed the legacy `-tf.reduce_sum(y * tf.log(y_pred))` formulation become NaN when the softmax output contained exact zeros.

## Observed behavior

- Running ./run_repro.sh installed TensorFlow 2.16.1 and reproduced the unstable loss calculation: softmax = [[1.0, 0.0, 0.0, 0.0]], unstable_loss = nan, stable_loss = [0.0], unstable_is_nan = True.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
