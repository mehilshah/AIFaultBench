# Bug 630

This folder reproduces Pyro issue 2815 from the local `codebase/` snapshot.

Observed failure:
- `ValueError: Error while computing log_prob at site 'measurement': The value argument to log_prob must be a Tensor`

What the repro uses:
- Python 3.11
- `torch==1.13.1+cpu`
- local Pyro source from `codebase/`

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

The failure comes from the intro tutorial using a Python float in
`pyro.condition(scale, data={"measurement": 9.5})` instead of a tensor.
