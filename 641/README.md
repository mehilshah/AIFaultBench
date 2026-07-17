# Bug 641

This folder contains a standalone reproduction bundle for:
`https://github.com/pytorch/rl/issues/3238`

Contents:
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

Reproduction summary:
- The bug reproduces in the local checkout.
- `MultiSyncDataCollector(..., split_trajs=True).set_seed(42)` fails during the first iteration.
- Failure signature: `RuntimeError: split_with_sizes expects split_sizes to sum exactly to 200 ... got split_sizes=[100, 50, 100, 50]`

Run:
`bash run_repro.sh`
