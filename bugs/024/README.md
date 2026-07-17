# Bug 024

This folder contains a self-contained reproduction bundle for the DELF import
failure reported in tensorflow/models issue 10852.

Root inputs:
- `bug_report.txt`
- `codebase/`

Generated repro artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Repro summary:
- The source tree contains `codebase/research/delf/delf/python/datasets/`, but
  that directory does not have an `__init__.py`.
- `codebase/research/delf/setup.py` uses `find_packages()`, which excludes that
  package from an installed distribution.
- Importing `delf` from the built install fails when `delf/__init__.py` tries to
  import `delf.python.datasets`.

Run:
```bash
bash run_repro.sh
```
