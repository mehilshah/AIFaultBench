# Reproduction Trajectory — Bug 690: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6709](https://github.com/langchain-ai/langgraph/issues/6709)
- **Repository:** langchain-ai/langgraph @ `30355a7a5df0c7ec49eba125e546c58b7360c10e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to start cloning the requested LangGraph checkout. The full-clone pack reached 331 MiB before a checkout was available, so this package-level issue uses the allowed issue-era released-package route.
2. Created an isolated Python 3.12 environment and installed `langgraph-api==0.7.6`, the issue-era public API package containing the edition selector. This released package was used because the report concerns the public runtime package, not an LLM or a service endpoint.
3. Set `LANGGRAPH_RUNTIME_EDITION=postgres` before importing `langgraph_runtime`.
4. Asserted that importing the selector raises the exact error naming the unavailable `langgraph-runtime-postgres` package.

## Observed behavior

- The final run exited with status 1 and printed `OBSERVED BUG: ImportError: Langgraph runtime backend not found. Please install with \`pip install "langgraph-runtime-postgres"\``.
- No network, provider API, model, database, or Redis call occurs; the failure happens during module resolution.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
