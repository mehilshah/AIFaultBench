# Reproduction Trajectory — Bug 764: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/11792](https://github.com/langflow-ai/langflow/issues/11792)
- **Repository:** langflow-ai/langflow @ `0a4dbc8c6c95d2576e180dccb04f2ae1f6ffa47f`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out the pinned Langflow revision.
2. Created `.venv` and installed `uv==0.9.1`, the version identified by the linked uv failure.
3. Ran `uv build --wheel` against `src/backend/base` with an empty, temporary `UV_CACHE_DIR`, which invokes the configured `hatchling.build` backend in build isolation.

## Observed behavior

- The build completed successfully with exit status 0; it did not raise `ModuleNotFoundError: No module named 'hatchling.build'`.
- The final script printed `NOT REPRODUCED: uv 0.9.1 built langflow-base with a fresh isolated cache`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The issue discussion identifies a corrupted uv/Podman build cache as the prerequisite. The pinned project correctly declares `hatchling` as a build requirement, and the fresh isolated cache on this machine has no corrupted cache entry to trigger the reported import failure.
