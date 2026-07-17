# Reproduction Trajectory — Bug 215: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2453](https://github.com/sdv-dev/SDV/issues/2453)
- **Repository:** sdv-dev/SDV @ `1114b57`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded the local SDV metadata modules from `codebase/` with minimal import stubs for unrelated optional dependencies.
2. Constructed metadata with two relationships that both point `C.parent_id` at different parent tables (`A` and `B`).
3. Called `Metadata.validate()` and observed that it completed successfully instead of rejecting the schema.

## Observed behavior

- Running `bash run_repro.sh` prints `VALIDATE_OK` and `BUG_REPRODUCED: duplicated foreign key reuse was accepted`, which means `Metadata.validate()` did not raise `InvalidMetadataError` for the reused child foreign key.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
