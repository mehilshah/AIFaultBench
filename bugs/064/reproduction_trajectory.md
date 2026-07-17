# Reproduction Trajectory — Bug 064: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1443](https://github.com/keras-team/keras-io/issues/1443)
- **Repository:** keras-team/keras-io @ `c36c0c95a73944e99452afe6d87c17bcc93c4e3a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build and save the NER Transformer model with a one-token trace input.
2. Load the SavedModel and convert it to TFLite.
3. Inspect the TFLite input tensor and confirm it is fixed to shape [1, 1].
4. Feed a 9-token int64 sample input and observe the dimension mismatch error.

## Observed behavior

- In the Dockerized TensorFlow 2.13.0 run, the exported TFLite model reported input shape [1, 1] with dtype int64. Passing a 9-token sample input raised `ValueError: Cannot set tensor: Dimension mismatch. Got 9 but expected 1 for dimension 1 of input 0.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
