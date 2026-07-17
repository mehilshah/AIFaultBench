# Bug 398

This folder contains a self-contained reproduction bundle for the Detectron2 cascade
ROI-head inference crash reported in issue 1132.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction strategy:
- Load the bundled Cascade R-CNN config from `codebase/configs/Misc/`.
- Call `CascadeROIHeads._forward_box` with dummy tensors and stubs.
- The code fails exactly where the bug report describes: `CascadeROIHeads` reads
  `self.test_score_thresh`, but this revision never defines it.

Source summary:
- issue URL: `https://github.com/facebookresearch/detectron2/issues/1132`
- commit hash: `e12b2d6534b5fb1c0e6bdc8f486986433e502d1a`
- library: `detectron2`
- library version: `0.1.1`
- bug report source: `bug_report.txt`
- codebase source: `facebookresearch/detectron2@e12b2d6534b5fb1c0e6bdc8f486986433e502d1a`
