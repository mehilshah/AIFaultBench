# Reproduction Trajectory — Bug 494: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2763](https://github.com/sdv-dev/SDV/issues/2763)
- **Repository:** sdv-dev/SDV @ `471d2e8d6ecec261a12287c337de3e5071a9b33f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtualenv with `./setup_env.sh`.
2. Run `./run_repro.sh` from the standardized bug folder.
3. Observe Ruff format check failures and the printed diffs in `repro_stdout.log`.

## Observed behavior

- Exit code 1 from `./run_repro.sh`. Ruff reported 5 files that would be reformatted: `EVALUATION.md`, `README.md`, `sdv/sequential/par.py`, `tests/_external/gdrive_utils.py`, and `tests/unit/datasets/test_demo.py`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
