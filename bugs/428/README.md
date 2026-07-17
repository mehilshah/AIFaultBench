# Bug 428

This folder contains a self-contained reproduction bundle for the Detectron2 `PolygonMasks.device` crash described in `bug_report.txt`.

Files in this folder:
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

Reproduction summary:
- issue URL: `https://github.com/facebookresearch/detectron2/issues/856`
- code under test: `codebase/detectron2/structures/masks.py`
- failing member: `PolygonMasks.device`
- observed exception: `AttributeError: 'PolygonMasks' object has no attribute 'tensor'`

Run:
`bash run_repro.sh`
