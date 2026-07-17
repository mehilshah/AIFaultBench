# Reproduction Trajectory — Bug 259: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2473](https://github.com/sdv-dev/SDV/issues/2473)
- **Repository:** sdv-dev/SDV @ `b756c57`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with setup_env.sh.
2. Install the runtime dependencies from requirements.txt and the local codebase in editable mode.
3. Run repro.py against a table with an all-null modeled column and call PARSynthesizer.sample(num_sequences=2).

## Observed behavior

- PARSynthesizer.sample() raises KeyError for the all-null modeled column at codebase/sdv/sequential/par.py:509.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
