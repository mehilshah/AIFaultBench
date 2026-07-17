# Reproduction Trajectory — Bug 311: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2856](https://github.com/sdv-dev/SDV/issues/2856)
- **Repository:** sdv-dev/SDV @ `5b85738576fc67e7be37d66328dab839841db3ff`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny multi-table dataset with a one-hot constrained Actions table.
2. Fit HMASynthesizer with OneHotEncoding(column_names=['Starts', 'SubstituteOn'], table_name='Actions').
3. Sample synthetic data, validate it, and run the multi-table diagnostic report.
4. Observe that the overall diagnostic score is below 1.0 and the Actions table TableStructure metric is 0.42857142857142855.

## Observed behavior

- The repro completed successfully and the multi-table diagnostic score was 0.9047619047619048, with the Actions table's Data Structure / TableStructure score at 0.42857142857142855.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
