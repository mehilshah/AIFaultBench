# Reproduction Trajectory — Bug 211: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/1910](https://github.com/sdv-dev/SDV/issues/1910)
- **Repository:** sdv-dev/SDV @ `f758807`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the sequential demo dataset nasdaq100_2019.
2. Add a categorical column named category containing alternating float values 100.0 and 50.0.
3. Fit PARSynthesizer(metadata) on the modified data and sample 2 sequences.
4. Run run_diagnostic(real_data, sampled_data, metadata) and inspect the Data Validity details.

## Observed behavior

- Running PARSynthesizer on the nasdaq100_2019 sequential demo with an added float categorical column produced synthetic category values outside {50.0, 100.0}. The captured diagnostic report shows Data Validity -> category CategoryAdherence = 0.0 and an overall diagnostic score of 0.9285714285714286.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
