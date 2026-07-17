# Reproduction Trajectory — Bug 017: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11038](https://github.com/tensorflow/models/issues/11038)
- **Repository:** tensorflow/models @ `272c3fab3557a09d4fa4260418836f74d7c4a503`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local virtual environment with `./setup_env.sh` and installed TensorFlow 2.21.0 plus the small runtime dependencies.
2. Ran `./run_repro.sh` against the bundled TensorFlow Models checkout and local sample image.
3. Verified that inference produced non-empty detection outputs instead of the empty tensors described in the report.

## Observed behavior

- Running `./run_repro.sh` completed successfully on Python 3.12.3 with TensorFlow 2.21.0.
- The object detection SavedModel loaded from `ssd_mobilenet_v1_coco_2017_11_17` and inference on `codebase/research/object_detection/test_images/image1.jpg` returned `num_detections=100` with `max_score=0.9406895041465759`.
- The detection tensors were populated, with example outputs `detection_scores[:5]=[0.9407 0.9345 0.2309 0.2252 0.1725]` and `detection_classes[:5]=[18, 18, 18, 18, 18]`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```

## Why it does not reproduce on the reference machine

The current checkout does not reproduce the reported TF1-era empty-tensor behavior; the TF2 SavedModel inference path returns populated detections on the local sample image.
