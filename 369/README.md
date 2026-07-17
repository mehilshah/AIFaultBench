# Bug 369

Reproduction bundle for Detectron2 issue [#2154](https://github.com/facebookresearch/detectron2/issues/2154).

Observed behavior in this folder:
- `iou1` prints `0.600224`
- `iou2` prints `1.000000`
- the expected value for both cases is `1.0`

Files in this bundle:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run order:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The repro uses the local source tree under `codebase/` and installs only the runtime dependencies needed for the snippet.
