# Bug 576

This folder contains a standalone reproduction bundle for the TorchRL replay-buffer hook bug reported in issue `#3247`.

What is included:
- `bug_report.txt`
- `codebase/`
- Generated repro artifacts:
  - `repro.py`
  - `requirements.txt`
  - `setup_env.sh`
  - `run_repro.sh`
  - `reproduction.json`
  - `repro_stdout.log`
  - `repro_stderr.log`

Observed failure:
- `ReplayBuffer.register_save_hook(TED2Flat())` raises `AttributeError: 'LazyMemmapStorage' object has no attribute 'register_save_hook'`

Reproduction command:
- `./run_repro.sh`

Source summary:
- issue URL: `https://github.com/pytorch/rl/issues/3247`
- commit hash: `7e0968aa621c0b67313b3f5db09d931baf8a1b3b`
- inferred library: `torchrl`
- inferred library version: `0.10.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
