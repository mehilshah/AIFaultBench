# Bug 415

Repro for NumPyro issue 2088:
`Beta(1.0, 8.0).log_prob(0.)` returns `nan` instead of a finite boundary value.

## Contents

- `bug_report.txt`: original issue summary
- `codebase/`: upstream NumPyro checkout at `ee8dbcb9a53dd42abc7a8ae2ffb9585a24ff3490`
- `requirements.txt`: pinned environment that reproduces the bug
- `setup_env.sh`: creates `.venv` and installs dependencies
- `repro.py`: minimal failing script
- `run_repro.sh`: convenience wrapper to run the repro
- `reproduction.json`: machine-readable reproduction result

## Reproduce

```bash
bash setup_env.sh
bash run_repro.sh
```

The failing case is:

```python
import numpyro.distributions as dist
dist.Beta(1.0, 8.0).log_prob(0.)
```

With the pinned environment, this evaluates to `nan`.
