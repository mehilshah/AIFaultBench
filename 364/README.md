# Bug 364 Repro

Issue: `accelerate` crashes in `_get_named_parameters()` when traversing a model that contains a `None` submodule.

The original report hit this through `load_checkpoint_and_dispatch()` while loading a Diffusers VAE test. This bundle isolates the same failure with a small PyTorch module so it can be reproduced without the full GPU test setup.

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

Reproduction:
1. Run `bash setup_env.sh`
1. Run `bash run_repro.sh`

Expected result:
- `load_checkpoint_and_dispatch()` raises `AttributeError: 'NoneType' object has no attribute '_parameters'`

Notes:
- The bug is in `codebase/src/accelerate/utils/modeling.py`.
- The repro is CPU-only; the report mentions GPU because the failure was observed in a GPU-backed test, but the underlying crash happens before device placement matters.
