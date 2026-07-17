# Reproduction Trajectory — Bug 214: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2434](https://github.com/sdv-dev/SDV/issues/2434)
- **Repository:** sdv-dev/SDV @ `c1acb42`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded the reported metadata and input data.
2. Instantiated GaussianCopulaSynthesizer.
3. Called fit(data) and observed a KeyError during regex parsing.

## Observed behavior

- KeyError: SUBPATTERN
- Traceback shows the failure originates in rdt.transformers.utils.strings_from_regex()

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
