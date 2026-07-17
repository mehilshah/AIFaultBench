# Reproduction Trajectory — Bug 358: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2849](https://github.com/sdv-dev/SDV/issues/2849)
- **Repository:** sdv-dev/SDV @ `8436e56d4755ec641f9524576d93effff99a3494`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a small one-hot dataframe with integer values.
2. Detect single-table metadata and set the one-hot columns to sdtype='numerical' with computer_representation='Int64'.
3. Add OneHotEncoding(column_names=['a', 'b', 'c']) to GaussianCopulaSynthesizer and call fit().

## Observed behavior

- Running the local repro raises ValueError during GaussianCopulaSynthesizer.fit(): "The column 'a' contains float values [0.9999998807907104, 1.1920928955078125e-07, 1.1920928955078125e-07]. All values represented by 'Int64' must be integers." The traceback is captured in repro_stderr.log.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
