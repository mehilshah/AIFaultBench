# POT Issue 82 Repro

This folder contains a standalone reproduction of PythonOT/POT issue 82.

What the repro does:
- loads the two distance matrices from the original Colab notebook export
- applies small compatibility shims needed for this old POT snapshot on modern NumPy/SciPy
- calls `ot.gromov.gromov_wasserstein(dists0, dists1, ...)`
- reproduces `TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'`

Files in the bundle:
- `bug_report.txt`
- `codebase/`
- `dists0.txt`
- `dists1.txt`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to run:
1. `bash run_repro.sh`
2. Inspect `repro_stdout.log` and `repro_stderr.log`

Observed result in this environment:
- same-matrix call succeeds
- slightly different matrices fail in `ot.optim.cg` when `alpha` comes back `None`

Source summary:
- issue URL: `https://github.com/PythonOT/POT/issues/82`
- notebook source: Colab export from `1IhnOqeLV51gWE8FodnBsgR5cQC_w2EkL`
- library: `POT`
- library version in source tree: `0.5.1`
