# Reproduction Trajectory — Bug 398: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/1132](https://github.com/facebookresearch/detectron2/issues/1132)
- **Repository:** facebookresearch/detectron2 @ `e12b2d6534b5fb1c0e6bdc8f486986433e502d1a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh

## Observed behavior

- repro_stdout.log shows: Loaded config ..., ROI head name: CascadeROIHeads, Cascade stages: 3, then AttributeError: 'CascadeROIHeads' object has no attribute 'test_score_thresh'. repro_stderr.log confirms the exception is raised from codebase/detectron2/modeling/roi_heads/cascade_rcnn.py line 149.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
