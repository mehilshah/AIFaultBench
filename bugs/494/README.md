# Reproduction Bundle

This folder reproduces the style-check failure described in `bug_report.txt`.

## What Fails

Running Ruff's formatter check against the provided `codebase/` reports files that would be reformatted.

## Setup

```bash
./setup_env.sh
```

## Reproduce

```bash
./run_repro.sh
```

## Expected Output

The command exits non-zero and prints a diff for files such as:

- `EVALUATION.md`
- `README.md`
- `sdv/sequential/par.py`
- `tests/_external/gdrive_utils.py`
- `tests/unit/datasets/test_demo.py`
