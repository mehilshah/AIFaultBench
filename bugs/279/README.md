# Bug 279

This folder contains the standardized reproduction bundle for the reported
`ColumnFormula` constraint crash.

## Outcome

The bug is **not reproducible** in this standardized folder.

## Why

The supplied `codebase/` is open-source SDV `1.37.3.dev1`. It does not export
`ColumnFormula` and does not contain an `sdv.cag.sandbox` module, so the
enterprise-only code path from the bug report is not available here.

## Artifacts

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

## Run

```bash
bash run_repro.sh
```
