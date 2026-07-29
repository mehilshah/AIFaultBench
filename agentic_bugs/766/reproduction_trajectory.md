# Reproduction Trajectory — Bug 766: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6434](https://github.com/langchain-ai/langgraph/issues/6434)
- **Repository:** langchain-ai/langgraph @ `0d4ac836e3a943a6a807910001f84a1d11b52776`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the initial network fetch left an unborn checkout, so fetched and detached the required pinned commit before testing.
2. Created an isolated Python 3.12 virtual environment, installed the exact pinned runtime dependencies, and installed the local `libs/langgraph` checkout in editable mode.
3. Ran `bash run_repro.sh`, which imports `CompiledStateGraph` from the `langgraph.graph` package namespace and asserts the expected failure.

## Observed behavior

- `bash run_repro.sh` exited with status 1.
- Standard output reported `OBSERVED ImportError: cannot import name 'CompiledStateGraph' from 'langgraph.graph' (/users/grad/mehil/MSR-MiningChallenge-2027/agentic_bugs/766/codebase/libs/langgraph/langgraph/graph/__init__.py)`.
- Standard error contained only a third-party `LangChainPendingDeprecationWarning`; it did not affect the assertion.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
