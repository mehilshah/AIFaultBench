# Bug 554

This folder contains a self-contained reproduction bundle for the PyG
`DistNeighborLoader` RPC unpack failure.

Source inputs reused from the standardized bug folder:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- The failing line is `torch_geometric/distributed/rpc.py: rpc_partition_to_workers`.
- The local repro boots RPC in a single-process configuration and injects a
  `None` entry into the gathered worker map.
- That drives the same `TypeError: cannot unpack non-iterable NoneType object`
  seen in the issue report.

Usage:
1. `bash setup_env.sh`
2. `bash run_repro.sh`
