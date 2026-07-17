# Bug 210

This folder contains a standalone reproduction for the `LazyMemmapStorage`
scratch-dir reuse bug reported in
[`bug_report.txt`](./bug_report.txt).

What the repro does:
- creates a temporary memmap scratch directory
- writes a `TensorDict` with keys `a` and `d`
- reuses the same scratch directory in a second `LazyMemmapStorage`
- writes a partial `TensorDict` missing key `d`
- shows that `storage["d"]` retains stale values instead of zeroing the missing rows

Files in this bundle:
- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`reproduction.json`](./reproduction.json)
- [`repro_stdout.log`](./repro_stdout.log)
- [`repro_stderr.log`](./repro_stderr.log)

Verified command:
- `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/pytorch/rl/issues/2437`
- inferred library: `torchrl`
- verified library version: `0.5.0`
