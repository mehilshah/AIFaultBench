# Bug 583

This folder is the reusable standardized benchmark input for the diffusers trust_remote_code bypass report.

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

Observed behavior:
- the normal remote-repo branch raises `ValueError` when `trust_remote_code=False`
- the community pipeline branch returns `diffusers_modules/git/clip_guided_stable_diffusion.py` instead of raising

Reproduction command:
- `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/huggingface/diffusers/issues/13691`
- commit hash: `5bd51bd189ab217e6e0ae708dceeb429689c00f7`
- library: `diffusers`
- library version: `0.39.0.dev0`
- bug report source: `bug_report.txt`
- codebase source: `huggingface/diffusers@5bd51bd189ab217e6e0ae708dceeb429689c00f7`
