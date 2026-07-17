# Reproduction Trajectory — Bug 226: unsloth

- **Bug report:** [https://github.com/unslothai/unsloth/issues/3488](https://github.com/unslothai/unsloth/issues/3488)
- **Repository:** unslothai/unsloth @ `69a6475`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a Python 3.9 venv with `bash setup_env.sh`.
2. Ran the repro harness with `bash run_repro.sh`.
3. Observed a successful install instead of the reported failure.

## Observed behavior

- In a Python 3.9.25 virtual environment, `uv pip install --python .venv/bin/python -r requirements.txt` completed successfully.
- `repro_stdout.log` records `repro_exit_code=0`.
- `repro_stderr.log` shows `Resolved 87 packages` and `Installed 84 packages`, including `unsloth==2026.1.2` and `unsloth-zoo==2026.1.2`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The current package release no longer reproduces the Python 3.9 install breakage described in the bug report. The dependency resolution succeeds on Python 3.9 in this environment, so there is no failure to block on.
