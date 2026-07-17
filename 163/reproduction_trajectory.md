# Reproduction Trajectory — Bug 163: keras-cv

- **Bug report:** [https://github.com/keras-team/keras-cv/issues/2370](https://github.com/keras-team/keras-cv/issues/2370)
- **Repository:** keras-team/keras-cv @ `9dd547a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create YOLOV8Detector with YOLOV8Backbone.from_preset('yolo_v8_xs_backbone').
2. Run the model on a 512x512 ones image.
3. Export the model with tf.saved_model.save and inspect the SavedModel using tensorflow.python.tools.saved_model_cli.

## Observed behavior

- A forward pass from YOLOV8Detector produced raw boxes with shape (1, 5376, 64).
- The exported SavedModel signature reported outputs['boxes'] tensor_info with shape (-1, -1, 64).
- The same export reported outputs['classes'] tensor_info with shape (-1, -1, 20).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
