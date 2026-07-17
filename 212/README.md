# Bug 212

This folder contains the reusable reproduction bundle for
`https://github.com/sdv-dev/SDV/issues/2290`.

What is included:
- `bug_report.txt`
- `codebase/`
- `ctgan/` and `deepecho/` test doubles that keep the import surface small
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- `HMASynthesizer` built from `MultiTableMetadata` still emits repeated
  `SingleTableMetadata` deprecation warnings during `sample()`.
- The bundled repro uses a tiny parent/child schema and captures the warning
  count in a deterministic way.

Run locally:
1. `bash setup_env.sh`
2. `bash run_repro.sh`

Expected result:
- `sample_warning_count` is greater than `1`
- `reproduction.json` records the bug as reproducible
