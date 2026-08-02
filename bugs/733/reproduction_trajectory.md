# Reproduction Trajectory — Bug 733: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/5933](https://github.com/mem0ai/mem0/issues/5933)
- **Repository:** mem0ai/mem0 @ `8d6b7c1d671af329dbf43a984fe1b3207ef59fe7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the report and maintainer triage note, which identify `Mem0Config.version` as the integer field and `set_nested_value()` as the faulty coercion path.
2. Recreated the pinned checkout. The mandated full clone transfer was interrupted on this host, so a filtered Git checkout fetched and checked out the same pinned commit.
3. Created `.venv`, installed the exact pinned build requirements, and installed `codebase/cli/python` editable without its unused CLI runtime dependencies.
4. Ran `set_nested_value(Mem0Config(), "version", "abc")` through `bash run_repro.sh` and captured its output.

## Observed behavior

- `run_repro.sh` exited with status 1 after printing `BUG REPRODUCED: set_nested_value raised ValueError: invalid literal for int() with base 10: 'abc'`.
- The traceback identifies `codebase/cli/python/src/mem0_cli/config.py`, line 238, where `int(value)` raises `ValueError`; the initial `version` value remained unchanged before the failing conversion.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
