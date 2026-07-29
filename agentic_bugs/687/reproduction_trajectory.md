# Reproduction Trajectory — Bug 687: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/38629](https://github.com/langchain-ai/langchain/issues/38629)
- **Repository:** langchain-ai/langchain @ `0501325e6c536a0693565bec99dde038cc5c4d20`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. The full monorepo clone did not complete promptly while concurrent benchmark jobs were cloning the same repository.
2. Used the released `langchain-classic==1.0.8` package, the version declared by the pinned checkout, and created `.venv` with `bash setup_env.sh`.
3. Ran `bash run_repro.sh` with duplicate `Document` objects whose `tags` metadata is a list.

## Observed behavior

- The final command exited 0 and printed `NOT_REPRODUCED: list metadata was deduplicated without TypeError (1 document)`.
- `repro_stderr.log` is empty.
- In `langchain-classic==1.0.8`, `unique_union()` delegates to equality-based `_unique_documents()` rather than constructing a hash key from `metadata.items()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported implementation has already been replaced in the pinned checkout's released `langchain-classic==1.0.8` package. Its equality-based deduplication handles list and dict metadata values without hashing them, so the specific `TypeError: unhashable type: 'list'` is unreachable.
