# Bug 247 Reproduction Bundle

This folder reproduces the `pyro.poutine.equalize` API gap described in
[`bug_report.txt`](./bug_report.txt).

Observed outcome:
- `pyro.poutine.equalize` is not defined in this checkout.
- The repro script raises `AttributeError` when it tries to call the requested handler.

Layout:
- [`repro.py`](./repro.py) contains the minimal failure case.
- [`setup_env.sh`](./setup_env.sh) creates an isolated virtual environment and installs runtime dependencies.
- [`run_repro.sh`](./run_repro.sh) runs the repro and writes logs to [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).
- [`reproduction.json`](./reproduction.json) records the schema-constrained result.

Run:
```bash
bash run_repro.sh
```

The repro uses the local `codebase/` checkout directly via `PYTHONPATH`, so no
application files are modified.
