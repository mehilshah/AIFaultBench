# Bug 189

This folder is the reusable standardized benchmark input for this bug.

Reused from the raw benchmark folder:
- `bug_report.txt`
- `codebase/` when available

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/mlfoundations/open_clip/issues/998`
- commit hash: `not found in Dataset.csv`
- inferred library: `open_clip_torch`
- inferred library version: `2.29.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase`

Repro summary:
- The second training run fails while loading `codebase/logs/repro_train1/checkpoints/epoch_1.pt`.
- The failure comes from `torch.load(..., weights_only=True)` inside `open_clip.factory.load_state_dict()`.
- Run `bash run_repro.sh` after the environment is prepared.
