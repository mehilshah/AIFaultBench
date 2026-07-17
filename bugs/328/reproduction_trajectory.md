# Reproduction Trajectory — Bug 328: POT

- **Bug report:** [https://github.com/PythonOT/POT/issues/24](https://github.com/PythonOT/POT/issues/24)
- **Repository:** PythonOT/POT @ `a29e22db4772ebc4a8266c917e2e662f624c6baa`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a virtualenv in `.venv` and installed the pinned repro dependencies.
2. Built the bundled POT Cython extension in place with `codebase/setup.py build_ext --inplace`.
3. Ran `repro.py`, which applies SciPy/NumPy compatibility shims and executes the issue 24 OTDA example.

## Observed behavior

- With compatibility shims for modern SciPy/NumPy, `repro.py` printed `sum(opt.G)=0.7333999999999999` and `result=reproduced`, so the coupling mass is below the expected 1.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
