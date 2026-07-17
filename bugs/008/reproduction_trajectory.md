# Reproduction Trajectory — Bug 008: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11141](https://github.com/tensorflow/models/issues/11141)
- **Repository:** tensorflow/models @ `5c0617a8f3041bfa97db45748050b9c254cb95d6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded codebase/research/object_detection/configs/tf2/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.config.
2. Executed ./run_repro.sh.
3. Observed the expected ValueError from the TF2 TFLite export guard.

## Observed behavior

- stdout showed the Faster R-CNN TF2 config being loaded and identified as model type faster_rcnn.
- stderr ended with ValueError: Only ssd or center_net models are supported in tflite. Found faster_rcnn in config.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
