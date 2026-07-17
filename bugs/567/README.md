# Bug 567

This folder contains a minimal reproduction bundle for
https://github.com/pyg-team/pytorch_geometric/issues/9933.

What the repro does:
- uses the local `codebase/` snapshot
- exercises `torch_geometric.nn.PNAConv`
- targets `cuda:1`, which is the device index called out in the report

Current workspace status:
- the system Python `torch` install is broken in this environment
- only one CUDA device is visible here, so `cuda:1` cannot be exercised

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

To reproduce in a fresh environment:
1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

The repro script prints a JSON summary and exits with:
- `1` if the illegal memory access is observed
- `2` if the environment is blocked before the target path can run
