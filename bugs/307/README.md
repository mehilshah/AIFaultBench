# Bug 307

This folder is the reusable standardized benchmark input for this Detectron2 visualizer bug.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How the repro works:
- It loads `codebase/detectron2/utils/visualizer.py` directly.
- It stubs unrelated imports that are not needed for the visualizer code path.
- It calls `Visualizer(..., instance_mode=ColorMode.IMAGE_BW)` on a synthetic mask.
- It compares the updated `VisImage.img` buffer to `VisImage.get_image()`.

Observed result:
- `IMAGE_BW` updates `self.output.img` to grayscale, but the rendered canvas returned by `get_image()` still shows the original image.
- That matches the bug report: the grayscale change is not reflected in the displayed output.

Reproduction command:
- `bash run_repro.sh`

Source metadata:
- issue URL: `https://github.com/facebookresearch/detectron2/issues/3486`
- commit hash: `ce5b1c5afe93919d14adf0fef27d608300a5171e`
