# Reproduction Trajectory — Bug 229: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/738](https://github.com/PythonOT/POT/issues/738)
- **Repository:** PythonOT/POT @ `e330215`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtualenv and install numpy==2.2.6, scipy==1.15.3, cython==3.2.8.
2. Install the local codebase editable package with pip install -e codebase.
3. Run bash run_repro.sh or repro.py in that environment.
4. Observe that the p=1 shared-shift check fails with a 0.005 absolute difference.

## Observed behavior

- With POT from the local codebase, wasserstein_circle(sample1, sample2) returns [0.095], while shifting both inputs by 0.02 returns [0.09] for p=1; the equality assertion from the report fails. The same inputs stay invariant for p=2.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
