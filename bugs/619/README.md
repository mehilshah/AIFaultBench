# Bug 619

This folder is a standalone repro bundle for the Lightning batch-size inference issue reported in
[`bug_report.txt`](./bug_report.txt).

Files:
- [`repro.py`](./repro.py): minimal validation-step reproducer
- [`requirements.txt`](./requirements.txt): runtime dependency pins
- [`setup_env.sh`](./setup_env.sh): creates a local virtualenv and installs deps
- [`run_repro.sh`](./run_repro.sh): runs the repro and captures stdout/stderr
- [`manifest.json`](./manifest.json): metadata for the standardized bug folder

Expected behavior:
- Running `bash run_repro.sh` emits the Lightning warning about inferring `batch_size` from an
  ambiguous collection.
- The warning should reference an inferred batch size of `3161` for the synthetic graph batch.
