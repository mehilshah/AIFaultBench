# Reproduction Trajectory — Bug 518: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2736](https://github.com/sdv-dev/SDV/issues/2736)
- **Repository:** sdv-dev/SDV @ `934ba74c5e3f0bc3c07f3b8e2ad204d3fec6006e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny two-table dataset and matching multi-table Metadata.
2. Fit an HMASynthesizer after adding both parent-table Inequality constraints in one call; this succeeds.
3. Add the same constraints in two separate add_constraints() calls on a fresh HMASynthesizer.
4. Call fit() and observe InvalidDataError from the single-table validation path inside preprocess().

## Observed behavior

- Control case: adding both Inequality constraints in one add_constraints() call fit successfully. Bug case: adding the same constraints in two separate add_constraints() calls crashed during fit() with InvalidDataError because the parent table metadata expected the first constraint's generated columns while the raw data still contained the original l1/h1 columns.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
