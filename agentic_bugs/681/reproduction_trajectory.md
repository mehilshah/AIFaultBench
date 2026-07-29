# Reproduction Trajectory — Bug 681: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/5931](https://github.com/mem0ai/mem0/issues/5931)
- **Repository:** mem0ai/mem0 @ `8d6b7c1d671af329dbf43a984fe1b3207ef59fe7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout at the supplied pinned commit.
2. Inspected `cli/python/src/mem0_cli/output.py`, which slices `mem.get("id", "")` and calls `len()` on the selected memory text without normalizing explicit nulls.
3. Created `.venv`, installed the pinned Rich dependency, and ran `repro.py` through `bash run_repro.sh`.
4. The local repro passed one record with `id`, `memory`, `created_at`, and `categories` set to `None` to each affected formatter; no API, model, provider, or network call occurs at runtime.

## Observed behavior

- `format_memories_text` raised `TypeError: 'NoneType' object is not subscriptable` from its null `id` field.
- `format_memories_table` raised `TypeError: object of type 'NoneType' has no len()` from its null `memory` field.
- `run_repro.sh` intentionally exited with status 1 after confirming both buggy failures.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
