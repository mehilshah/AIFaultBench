# Reproduction Trajectory — Bug 689: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6782](https://github.com/langchain-ai/langgraph/issues/6782)
- **Repository:** langchain-ai/langgraph @ `f9870bc9aefeb271927ffd5ad558b22e416793ef`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. The full source clone did not complete in the shared host's concurrent clone workload, so used the permitted released-package fallback, `langgraph==1.0.7`; its matching stack-frame line numbers verify the issue-era fault.
2. Created `.venv` and installed the fully pinned dependencies from `requirements.txt`.
3. Built a local one-node `StateGraph` and called `graph.invoke(None, config="invalid_config")`. This involves no model, provider, credential, or runtime network call.

## Observed behavior

- `run_repro.sh` exited with status 1 after printing `OBSERVED: AttributeError: 'str' object has no attribute 'items'`.
- The traceback reached `langgraph/_internal/_config.py:302` at `for k, v in config.items()`, through `main.py:2499` (`stream`) and `main.py:3071` (`invoke`).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
