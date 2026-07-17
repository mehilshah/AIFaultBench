# Bug 592 Reproduction Bundle

This folder contains a standalone reproduction for SDV issue 2708:
`[DayZ Parameters] 'missing_values_proportion' must be zero for any key columns`.

## Contents

- `bug_report.txt`: original issue report
- `codebase/`: local source snapshot used for the repro
- `repro.py`: minimal script that triggers the bug
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a virtual environment and installs dependencies
- `run_repro.sh`: runs the repro script
- `manifest.json`: metadata for the standardized bundle
- `reproduction.json`: schema-constrained result written after running the repro
- `repro_stdout.log` and `repro_stderr.log`: command output captured during reproduction

## Reproduction

```bash
bash setup_env.sh
bash run_repro.sh
```

The script intentionally mutates a generated DayZ parameter dictionary so the primary key has
`missing_values_proportion = 0.5`. The bug is present if validation succeeds instead of raising
`SynthesizerProcessingError`.

## Source Notes

- issue URL: `https://github.com/sdv-dev/SDV/issues/2708`
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
