# Reproduction Trajectory — Bug 369: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/2154](https://github.com/facebookresearch/detectron2/issues/2154)
- **Repository:** facebookresearch/detectron2 @ `a2648075f2e76c0fbcef89c84db2319d7b56cc17`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python virtual environment and install the runtime dependencies listed in `requirements.txt`.
2. Install the local detectron2 source tree in editable mode with `FORCE_CUDA=0 python -m pip install -e codebase --no-deps --no-build-isolation`.
3. Run `bash run_repro.sh` to execute the rotated-IoU snippet from the bug report.

## Observed behavior

- Running `bash run_repro.sh` prints `iou1: 0.600224` and `iou2: 1.000000`, then fails with `AssertionError: Expected both IoUs to be 1.0`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
