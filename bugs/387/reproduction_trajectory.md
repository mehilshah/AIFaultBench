# Reproduction Trajectory — Bug 387: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2826](https://github.com/sdv-dev/SDV/issues/2826)
- **Repository:** sdv-dev/SDV @ `b895858c1e306b64f5debf7adc78bdb2b9c78131`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Restore the referenced SDV snapshot with `bash setup_codebase.sh`.
2. Create a local virtualenv and install the lightweight repro dependencies with `bash setup_env.sh`.
3. Run `bash run_repro.sh` to execute the local metadata scenario.
4. Observe that the composite primary-key step is rejected before the reported relationship-validation bug can be reached.

## Observed behavior

- Running `bash run_repro.sh` prints `BLOCKED: current snapshot rejects composite primary keys before relationship` and `InvalidMetadataError: 'primary_key' must be a string.` from `codebase/sdv/metadata/single_table.py`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This checkout does not accept composite primary keys through the public single-table metadata API, so the reported scenario cannot be exercised here.
