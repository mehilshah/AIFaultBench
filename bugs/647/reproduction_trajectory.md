# Reproduction Trajectory — Bug 647: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/8089](https://github.com/langchain-ai/langgraph/issues/8089)
- **Repository:** langchain-ai/langgraph @ `97320843fe78b93bd5290ce366841ff9850bf379`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then fetched and checked out the prescribed commit because the initial clone had no fetched objects.
2. Created `.venv`, installed `langgraph-api==0.12.0.dev3` and `langgraph-runtime-inmem==0.31.0.dev9`, and installed the checkout's `langgraph-cli` 0.4.29 in editable mode.
3. Ran `bash run_repro.sh`, which executes the actual in-memory runtime lifespan. Its database, HTTP-client, checkpointer, and UI startup calls are async no-ops, so no services or third-party network calls occur before the compatibility check.

## Observed behavior

- The final run exited with status `1`.
- It printed `OBSERVED BUG: AttributeError: module 'langgraph_api.config' has no attribute 'LSD_PROM_METRICS_ENABLED'`.
- `repro_stderr.log` was empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
