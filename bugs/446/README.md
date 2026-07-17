# Bug 446

This folder contains the standardized reproduction bundle for SDV issue 2803.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Result:
- The reported `financial` demo column-order mismatch was not reproducible here.
- `download_demo(modality='multi_table', dataset_name='financial')` returned table columns in the same order as the metadata for every table checked.

How to run:
- `bash setup_env.sh`
- `bash run_repro.sh`

Source summary:
- issue URL: `https://github.com/sdv-dev/SDV/issues/2803`
- commit hash: `74744e5f87fa72bdff14d031eafeaa21a4085088`
- library: `SDV`
- library version: `1.33.1`
- bug report source: `bug_report.txt`
- codebase source: `sdv-dev/SDV@74744e5f87fa72bdff14d031eafeaa21a4085088`
