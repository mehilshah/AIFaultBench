# Bug 357

This folder reproduces the mypy syntax failure described in
`bug_report.txt`.

Observed failure:

- `mypy` exits with code `2`
- stderr includes:
  `.venv/lib/python3.12/site-packages/numpy/_typing/_nested_sequence.py:60: error: Positional-only parameters are only supported in Python 3.8 and greater  [syntax]`

The failure is caused by `codebase/setup.cfg` pinning:

```ini
[mypy]
python_version = 3.7
```

Reproduction:

```bash
bash setup_env.sh
bash run_repro.sh
```

Files in this folder:

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
