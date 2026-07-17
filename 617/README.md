# Bug 617

This folder contains the reusable reproduction bundle for Pyro issue 2833.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Confirmed reproduction:
- Pyro `1.6.0`
- torch `1.8.1+cpu`
- Python `3.9`
- NumPy `<2`

The failure occurs when Pyro patches `torch.distributions.constraints._PositiveDefinite.check` and reshapes a zero-element covariance tensor with `reshape((-1, 0, 0))`.
