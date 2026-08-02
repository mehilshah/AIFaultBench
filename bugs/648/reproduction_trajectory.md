# Reproduction Trajectory — Bug 648: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6342](https://github.com/langchain-ai/langgraph/issues/6342)
- **Repository:** langchain-ai/langgraph @ `5796ca9a0ad8ec53dbcf12fa9f1d671b826e5f1d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to clone the repository and check out the pinned buggy commit.
2. Created `.venv`, installed the exact pinned runtime dependencies, and installed the checked-out `libs/langgraph` package editable.
3. Ran `repro.py` through `bash run_repro.sh`. The script starts a loopback-only standard-library HTTP server, then calls `RemoteGraph.stream()` with `context` and `config={"configurable": {"thread_id": "bug-thread"}}`.
4. The local server verifies the exact outgoing request and responds with the API's documented 400 rejection when it contains both fields. The script checks the status and error detail, prints the observed fault, and raises an assertion so the command exits non-zero.

## Observed behavior

- `run_repro.sh` exited with status 1.
- The request reached `/threads/bug-thread/runs/stream` with both `context={"user_id": "123"}` and `config={"configurable": {"thread_id": "bug-thread"}}`.
- The observed result was HTTP 400 with `Cannot specify both configurable and context. Prefer setting context alone.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
