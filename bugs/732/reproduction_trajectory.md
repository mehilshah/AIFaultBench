# Reproduction Trajectory — Bug 732: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/6258](https://github.com/mem0ai/mem0/issues/6258)
- **Repository:** mem0ai/mem0 @ `17836748d7afe0521516c6a73c6a256680f05527`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. Its initial clone had no checked-out `HEAD` in this environment, so fetched and checked out the required pinned commit `17836748d7afe0521516c6a73c6a256680f05527`.
2. Created `.venv`, installed `pydantic==2.12.5`, and installed the pinned checkout editable without pulling optional vector-store dependencies.
3. Ran `bash run_repro.sh`; the script stubs only the optional `chromadb` import and calls the checkout's real `ChromaDB._generate_where_clause` method.

## Observed behavior

- Input `{'age': {'betwen': [10, 20]}}` returned `{'age': {'$eq': [10, 20]}}` rather than raising a `ValueError`.
- The repro prints `BUG REPRODUCED` and exits with status 1 by raising `AssertionError` after detecting the silent equality downgrade.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
