# Reproduction Trajectory — Bug 067: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1147](https://github.com/keras-team/keras-io/issues/1147)
- **Repository:** keras-team/keras-io @ `54392950c4142c96ccc0f8dfd4a9a586edbe5cf2`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a minimal TensorFlow repro in repro.py that compares sparse categorical crossentropy for squeezed and unsqueezed labels.
2. Ran setup_env.sh and run_repro.sh inside a local virtual environment.
3. Observed no runtime failure and no numerical difference between the two label shapes.

## Observed behavior

- TensorFlow 2.16.1 produced identical sparse categorical crossentropy losses for target shapes (1, 2, 2) and (1, 2, 2, 1); max_abs_diff was 0.0. See repro_stdout.log and repro.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported shape issue is not reproducible in this environment because the current TensorFlow build accepts the extra singleton label dimension and computes the same loss as the squeezed labels.
