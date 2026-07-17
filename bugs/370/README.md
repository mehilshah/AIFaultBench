# Bug 370

This folder contains a self-contained reproduction bundle for the LSTMModule bug
reported in torchrl issue 3711.

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

Verified result:
- The bug is reproducible in a clean CPU-only virtualenv.
- The final step of the shorter second trajectory has zeroed hidden state values.

Run locally:
`bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/pytorch/rl/issues/3711`
- codebase version: `0.12.0`
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
