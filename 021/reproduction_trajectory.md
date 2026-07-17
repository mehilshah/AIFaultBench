# Reproduction Trajectory — Bug 021: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/10947](https://github.com/tensorflow/models/issues/10947)
- **Repository:** tensorflow/models @ `ec549fd122da7c1987ba01246b7d26b7f8787e6a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean Python 3.12 virtual environment and install tensorflow-cpu==2.16.1.
2. Run repro.py through run_repro.sh from the standardized bug folder.
3. Observe the empty-list ConcatV2 InvalidArgumentError in repro_stderr.log.

## Observed behavior

- run_repro.sh completed and repro_stderr.log captured InvalidArgumentError from ConcatV2 with N=0 at official/vision/modeling/layers/detection_generator.py:518. The repro uses a single-class raw score tensor that becomes zero classes after the background slice, leaving tf.concat([]) in _generate_detections_v2_class_aware.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
