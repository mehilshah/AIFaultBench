# Reproduction Trajectory — Bug 296: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/117](https://github.com/PythonOT/POT/issues/117)
- **Repository:** PythonOT/POT @ `a9bbc2cfdffd22ceee3256102e470df6c25338f3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed numpy, scipy, and cython.
2. Installed the local POT codebase in editable mode with build isolation disabled.
3. Ran repro.py through ./run_repro.sh with a 50000 x 50000 zero cost matrix and empty histograms.
4. Observed the C++ solver abort with std::length_error / vector::_M_default_append.

## Observed behavior

- Running ./run_repro.sh prints 'allocating M 50000 x 50000' and 'calling ot.emd([], [], M)', then aborts with 'terminate called after throwing an instance of 'std::length_error'' and 'what():  vector::_M_default_append'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
