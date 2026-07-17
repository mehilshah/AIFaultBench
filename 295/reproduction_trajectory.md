# Reproduction Trajectory — Bug 295: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2868](https://github.com/sdv-dev/SDV/issues/2868)
- **Repository:** sdv-dev/SDV @ `2995df37bbc723fdffa6d91a86d143fd13dc63ce`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create `.venv` and install `pandas==2.3.3` plus `rdt==1.21.0`.
2. Run `bash run_repro.sh`.
3. Observe that `sdv._utils.get_possible_chars('(ab)*')` returns `['ab']` instead of raising `ValueError: REGEX operation: SUBPATTERN is not supported by SDV.`

## Observed behavior

- After installing the local requirements in .venv, `bash run_repro.sh` printed `observed result: ['ab']` for `get_possible_chars('(ab)*')` and then raised `AssertionError` because no `ValueError` was raised. This matches the bug report's failing test expectation under rdt==1.21.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
