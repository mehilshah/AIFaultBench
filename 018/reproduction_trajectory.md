# Reproduction Trajectory — Bug 018: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/11035](https://github.com/tensorflow/models/issues/11035)
- **Repository:** tensorflow/models @ `efe006c024494e6c513281251213df9af9c62a55`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Open codebase/research/object_detection/g3doc/tf2.md and find the install command.
2. Run python3 -m pip install --use-feature=2020-resolver . from codebase/research/object_detection/packages/tf2.
3. Observe pip fail before installation starts with invalid choice: '2020-resolver'.

## Observed behavior

- pip 26.1.2 rejects --use-feature=2020-resolver with invalid choice; the command exits with status 2.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
