# Reproduction Trajectory — Bug 260: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2601](https://github.com/sdv-dev/SDV/issues/2601)
- **Repository:** sdv-dev/SDV @ `41ce2b9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a parent/child multi-table dataset with `parent` containing `colA`, `colB`, and `colC`.
2. Detect metadata from the dataframes and instantiate `HMASynthesizer(metadata)`.
3. Add two overlapping `Inequality` constraints on the `parent` table: `colA < colB` and `colB < colC`.
4. Call `synthesizer.add_constraints([constraint1, constraint2])`.

## Observed behavior

- Running `bash run_repro.sh` prints `before add_constraints` and then fails with `sdv.cag._errors.ConstraintNotMetError: Table 'parent' is missing columns 'colB'.` The traceback originates in `sdv/multi_table/base.py:229` while applying the second overlapping `Inequality` constraint.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
