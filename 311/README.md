# Bug 311 Reproduction

This folder reproduces the OneHotEncoding diagnostic score regression from SDV issue 2856.

Observed result in this environment:
- `run_diagnostic(...)` returns a score below `1.0`
- `Data Structure -> Actions -> TableStructure` is `0.42857142857142855`

## Files

- `repro.py` runs the minimal multi-table fixture.
- `requirements.txt` installs the local SDV checkout and its runtime dependencies.
- `setup_env.sh` creates a virtual environment and installs dependencies.
- `run_repro.sh` runs the repro and writes `repro_stdout.log` and `repro_stderr.log`.
- `manifest.json` records the issue metadata for this benchmark folder.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
cat reproduction.json
```
