# Reproduction Trajectory — Bug 212: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2290](https://github.com/sdv-dev/SDV/issues/2290)
- **Repository:** sdv-dev/SDV @ `4d56fe7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a MultiTableMetadata schema with a parent table and a child table linked by a foreign key.
2. Instantiate HMASynthesizer with that MultiTableMetadata and fit it on the small two-table dataset.
3. Call sample() and capture warnings; the repro emits 6 SingleTableMetadata deprecation warnings during sampling.

## Observed behavior

- Running the bundled repro against the local SDV checkout produced 6 repeated FutureWarnings with the message "The 'SingleTableMetadata' is deprecated. Please use the new 'Metadata' class for synthesizers." during HMASynthesizer.sample().

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
