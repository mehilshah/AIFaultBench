# Reproduction Trajectory — Bug 058: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1594](https://github.com/keras-team/keras-io/issues/1594)
- **Repository:** keras-team/keras-io @ `26caa1591220a6469d8ecc508ca89f211681746c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a dense zero-box dataset with shape [2, 0, 4] for boxes and [2, 0] for classes.
2. Built keras_cv.models.RetinaNet with a no-download ResNet50 backbone preset.
3. Called model.fit for one step and observed the GatherV2 out-of-range failure in RetinaNetLabelEncoder.

## Observed behavior

- On TensorFlow 2.14.1 and KerasCV 0.6.4, fitting RetinaNet on a batch with zero ground-truth boxes triggers InvalidArgumentError at retina_net_label_encoder/GatherV2_1: indices[0,10000] = 0 is not in [0, 0).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
