# Reproduction Trajectory — Bug 457: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/334](https://github.com/facebookresearch/detectron2/issues/334)
- **Repository:** facebookresearch/detectron2 @ `dd5926a54ee2e346f51e01afb8c0ecbb17b87a37`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect `projects/DensePose/densepose/evaluation/densepose_coco_evaluation.py` and locate `pixel_embeddings = embedding[:, py, px].t().to(device="cuda")` in `findClosestVertsCse`.
2. Run `bash run_repro.sh` to execute the self-contained repro.
3. Observe `current_impl failed RuntimeError CUDA requested from a CPU-only tensor` and `cpu_safe_reference passed [-1, 11]` in `repro_stdout.log`.

## Observed behavior

- The DensePose evaluator hardcodes CUDA in `projects/DensePose/densepose/evaluation/densepose_coco_evaluation.py:1186`. The repro script confirmed the source line exists, then showed the current implementation fails on a CPU-only tensor with `RuntimeError CUDA requested from a CPU-only tensor`, while a CPU-safe reference path succeeds.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
