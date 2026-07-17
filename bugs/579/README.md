# Bug 579

Issue: https://github.com/sdv-dev/SDV/issues/2711

This bundle reproduces the pandas `FutureWarning` described in the bug report by
exercising the same `HMASynthesizer._clear_nans` fillna branch from
`codebase/sdv/multi_table/hma.py`.

## Repro steps

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

The repro is expected to print a JSON payload that includes the warning text:
`Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated ...`

## Notes

- The issue report referenced SDV `1.27.0`.
- The checked-in codebase snapshot reports `1.27.1.dev0` in `codebase/sdv/__init__.py`.
- The warning is observable on pandas `2.2.3`; the host pandas `3.0.3` no longer emits it.
