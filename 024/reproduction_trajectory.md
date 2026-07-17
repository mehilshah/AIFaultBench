# Reproduction Trajectory — Bug 024: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/10852](https://github.com/tensorflow/models/issues/10852)
- **Repository:** tensorflow/models @ `2229297fa2a8ab354dbf68e6d61db99c51e57b2c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the DELF source tree from codebase/research/delf without extra dependencies.
2. Import delf from the installed package using a stubbed runtime for TensorFlow and other unrelated libraries.
3. Observe that delf/__init__.py eventually imports delf.python.datasets and fails because that package is not present in the built distribution.

## Observed behavior

- importing the installed delf package fails with the expected ModuleNotFoundError

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
