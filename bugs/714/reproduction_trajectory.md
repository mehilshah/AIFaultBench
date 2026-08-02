# Reproduction Trajectory — Bug 714: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/12408](https://github.com/langflow-ai/langflow/issues/12408)
- **Repository:** langflow-ai/langflow @ `263cfc68f170110473a9a1a47c1d0f1b629ab548`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that the checkout was at the requested buggy commit.
2. Created an isolated virtual environment, installed the released `lfx==0.4.0` dependency set, and installed the checkout's `src/lfx` package editable so the code under test was the pinned source.
3. Called the real `Graph.astep` method on a minimal in-memory graph whose only vertex is frozen, while patching `get_chat_service` to return `None`.
4. Ran `bash run_repro.sh` and captured its non-zero output.

## Observed behavior

- The no-service fallback returned `None` for the frozen vertex cache lookup.
- `Graph.build_vertex` raised `TypeError: 'NoneType' object is not subscriptable` at `base.py:1565` while evaluating `cached_result["result"]`.
- The final command exited with status 1, after printing `BUG REPRODUCED: TypeError: 'NoneType' object is not subscriptable`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
