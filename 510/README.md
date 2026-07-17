# Bug 510

This folder reproduces SDV issue [#2739](https://github.com/sdv-dev/SDV/issues/2739):
`HMASynthesizer` emits the missing-`datetime_format` warning multiple times for the same column.

Files in this bundle:
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

Reproduction:
1. Run `bash setup_env.sh`.
2. Run `bash run_repro.sh`.

Observed result:
- the missing-`datetime_format` warning was captured 3 times for `main.denormalized_column`.
