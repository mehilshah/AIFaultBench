# Bug 627

Standardized repro bundle for:
`https://github.com/huggingface/pytorch-image-models/issues/2407`

Status:
- The reported `FileNotFoundError` from `timm/utils/checkpoint_saver.py` did not reproduce in this folder.
- The local probe completes a 5-epoch checkpoint rotation without error.

Contents:
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

How to run:
`bash run_repro.sh`

Notes:
- The probe uses a tiny local model and a temporary output directory to exercise the checkpoint saver without requiring the original 4xL40S / HF dataset setup.
- Because the bug did not reproduce locally, the bundle records a negative result rather than a failing trace.
