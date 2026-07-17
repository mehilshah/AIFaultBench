# Bug 443

This folder is the reusable standardized benchmark input for this bug.

Reused inputs:
- `bug_report.txt`
- `codebase/` at `83c2101d3ef92b25e371db24e0b6aca8112ea1dd`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Source summary:
- issue URL: `https://github.com/pytorch/rl/issues/3515`
- commit hash: `83c2101d3ef92b25e371db24e0b6aca8112ea1dd`
- library: `torchrl`
- library version: `0.11.0+g83c2101d3`
- reproduction: synthetic TensorDict path that matches the reported single-agent batch shape
