# Bug 596

This folder is the reusable standardized benchmark input for the diffusers offloading regression.

What is included:
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

Repro summary:
- The bug shows up in `UniPCMultistepScheduler.multistep_uni_p_bh_update`.
- On CUDA, the third scheduler step hits `torch.stack(rks)` with mixed devices (`cuda:0` and `cpu`).
- The minimal repro avoids model downloads and exercises only the scheduler path.

Run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`
