# Reproduction Trajectory — Bug 384: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/1207](https://github.com/facebookresearch/detectron2/issues/1207)
- **Repository:** facebookresearch/detectron2 @ `2ca36e3cbfb2c84c18502221564b629f3877e8be`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Restore the Detectron2 source tree with `bash setup_codebase.sh` when `codebase/` is absent.
2. Activate the preserved `.venv_repro` environment and build the `_C` extension in place if it is missing.
3. Run `python repro.py` through `bash run_repro.sh` to evaluate the exact rotated box pair from the issue report.

## Observed behavior

- Running `bash run_repro.sh` prints JSON with `actual_iou` equal to `0.26549291610717773` for the reported box pair, while `expected_iou` is `0.0`.
- The same run reports `wrote_image: true`, so the visualization path still succeeds and the mismatch is in `pairwise_iou_rotated`.
- The exact command output is captured in `repro_stdout.log`, and `repro_stderr.log` is empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
