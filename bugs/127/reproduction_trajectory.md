# Reproduction Trajectory — Bug 127: unknown

- **Bug report:** [https://github.com/exaloop/codon/issues/609](https://github.com/exaloop/codon/issues/609)
- **Repository:** exaloop/codon @ `d13d6a5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal Codon program in `repro.py` that matches the issue report.
2. Verified the local Codon binary with `./setup_env.sh`.
3. Ran `bash run_repro.sh` and captured output in `repro_stdout.log` and `repro_stderr.log`.

## Observed behavior

- Running `bash run_repro.sh` with Codon 0.19.6 prints `empty 0 0`, `int float 1 2`, `int float 1 2`, `int float 3 5`. The `Foo(1, 2)` and `Foo(a, b)` calls should select the `__init__(self, x: int, y: int)` overload, but they incorrectly select the `y: float` overload.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
