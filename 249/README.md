# Bug 249

This folder is a self-contained repro bundle for the TorchRL `MLP` default-construction issue reported in `bug_report.txt`.

Inputs reused from the benchmark source:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- issue URL: `https://github.com/pytorch/rl/issues/2328`
- inferred library: `torchrl`
- observed behavior: `MLP(in_features=1024, out_features=512)` expands to 3 hidden layers of width 32 by default
- expected behavior from report: a single linear layer from 1024 to 512
- validated environment: `torch==2.4.0`, `tensordict==0.5.0`
