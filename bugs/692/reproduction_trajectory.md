# Reproduction Trajectory — Bug 692: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6655](https://github.com/langchain-ai/langgraph/issues/6655)
- **Repository:** langchain-ai/langgraph @ `8ccead9560f6cd76537f632d7a310ba41e38f28b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; its clone did not yield a checkout `HEAD` on this host, so this released-package compatibility issue used the permitted issue-era package fallback.
2. Created `.venv` and installed the issue-era released packages from `requirements.txt`, including `langgraph==1.0.5`, `langgraph-api==0.6.20`, and `langgraph-runtime-inmem==0.21.0`.
3. Ran the real `Threads.State.list` history implementation with local stubs for auth and persistence only; this avoids a database, Studio server, LLM, or external network request while reaching its real `get_graph(...)` call.
4. Ran `bash run_repro.sh` and captured its non-zero final result.

## Observed behavior

- `run_repro.sh` exited with status `1` and printed `OBSERVED BUG: get_graph() missing 1 required keyword-only argument: 'is_for_execution'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
