# Bug 516 Reproduction Bundle

This folder reproduces the `MultiAgentNetBase` centralized shared-parameter shape expansion from
[`bug_report.txt`](./bug_report.txt) against the local [`codebase/`](./codebase) snapshot.

## Repro

1. `bash setup_env.sh`
1. `bash run_repro.sh`

## Expected Result

The minimal example should produce `output_shape=(4, 3, 4)`.

## Observed Result

The current source produces `output_shape=(4, 3, 3, 4)`, which duplicates the agent dimension in
centralized mode.

## Files

- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
