# Bug 471

This folder is the reusable standardized benchmark input for the detectron2 `RandomCrop.__repr__` bug.

Reused inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `support/`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/facebookresearch/detectron2/issues/92`
- commit hash: `2ac32f9d5a21154484a3bb2d4ab7c94c18c08119`
- library: `detectron2`
