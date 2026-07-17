# Reproduction Trajectory — Bug 257: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2096](https://github.com/sdv-dev/SDV/issues/2096)
- **Repository:** sdv-dev/SDV @ `0173c77`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a `SingleTableMetadata` object with column `A` defined as `id`.
2. Set both `primary_key` and `sequence_key` to `A`.
3. Run `./run_repro.sh` and observe that validation and the setter both succeed instead of raising `InvalidMetadataError`.

## Observed behavior

- `./run_repro.sh` prints `metadata.validate(): completed without error`.
- `./run_repro.sh` prints `set_primary_key('A'): completed without error`.
- `./run_repro.sh` prints `BUG REPRODUCED: primary_key and sequence_key can point to the same column.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
