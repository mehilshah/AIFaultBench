# Reproduction Trajectory — Bug 059: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1593](https://github.com/keras-team/keras-io/issues/1593)
- **Repository:** keras-team/keras-io @ `26caa1591220a6469d8ecc508ca89f211681746c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a BoxCOCOMetrics instance with bounding_box_format='xyxy'.
2. Call update_state twice with batches whose ground-truth boxes have different per-image counts.
3. Call result(force=True) and observe the concat failure.

## Observed behavior

- Running the minimal BoxCOCOMetrics repro under tensorflow==2.19.1, keras-cv==0.9.0, and pycocotools==2.0.11 raises InvalidArgumentError: ConcatOp : Dimension 1 in both shapes must be equal: shape[0] = [1,2,4] vs. shape[1] = [1,1,4]. The traceback points to keras_cv/src/metrics/object_detection/box_coco_metrics.py::_box_concat.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
