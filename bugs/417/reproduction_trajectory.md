# Reproduction Trajectory — Bug 417: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2823](https://github.com/sdv-dev/SDV/issues/2823)
- **Repository:** sdv-dev/SDV @ `b895858c1e306b64f5debf7adc78bdb2b9c78131`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Loaded SDV metadata from a dict with one table and two numerical columns.
2. Called Metadata.set_primary_key(['col1', 'col2']).
3. Observed InvalidMetadataError: 'primary_key' must be a string.

## Observed behavior

- See the captured logs below for the observed output.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The checkout raises 'primary_key' must be a string instead of the nested-list message described in the report.
