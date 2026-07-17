# Reproduction Trajectory — Bug 025: models

- **Bug report:** [https://github.com/tensorflow/models/issues/10860](https://github.com/tensorflow/models/issues/10860)
- **Repository:** tensorflow/models @ `9e0bc850e9a86c0cc50866eb3cc48c3c1a505110`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash run_repro.sh

## Observed behavior

- bash run_repro.sh printed HAS_AUGMENT=False and ERROR=AttributeError: module 'tensorflow_models.vision' has no attribute 'augment'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
