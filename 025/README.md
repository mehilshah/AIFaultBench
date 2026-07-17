# Bug 025

Repro bundle for TensorFlow Models issue 10860.

Observed failure:
`tensorflow_models.vision` is importable, but it does not expose `augment`, so `tfm.vision.augment.RandAugment()` raises `AttributeError`.

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

Reproduction command:
`bash run_repro.sh`
