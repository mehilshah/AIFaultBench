# Reproduction Trajectory — Bug 343: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2852](https://github.com/sdv-dev/SDV/issues/2852)
- **Repository:** sdv-dev/SDV @ `db5bcb22a86ca2a1f790f531f0df4a7bd6cc737d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Build a single-table dataset with boolean, categorical, and numerical columns.
2. Fit GaussianCopulaSynthesizer with FixedCombinations plus a row-dropping programmable constraint.
3. Call sample(20).
4. Observe pandas.errors.IndexingError from boolean index misalignment in reverse_transform_constraints.

## Observed behavior

- Sampling raised pandas.errors.IndexingError: Error: Sampling terminated. No results were saved due to unspecified "output_file_path".. The traceback reaches sdv/single_table/base.py:804 while applying reverse_transform_constraints.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```
