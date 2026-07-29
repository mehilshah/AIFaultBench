# Reproduction Trajectory — Bug 686: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/38644](https://github.com/langchain-ai/langchain/issues/38644)
- **Repository:** langchain-ai/langchain @ `0501325e6c536a0693565bec99dde038cc5c4d20`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; after its full repository transfer did not complete, fetched the same pinned commit shallowly and checked it out.
2. Created `.venv`, installed the exact pinned dependencies, and installed `libs/core` plus `libs/partners/anthropic` from that checkout editable.
3. Bound the report's `advisor_20260301` tool dictionary to `ChatAnthropic` with a dummy API key, without invoking a model.
4. Ran the final reproduction through `bash run_repro.sh` and captured its output.

## Observed behavior

- `bash run_repro.sh` exited with status 1, as required to signal the buggy behavior.
- It printed `OBSERVED BUG: bind_tools raised KeyError: 'parameters' for advisor_20260301`.
- The error is raised during `bind_tools`; no LLM/provider call is made and stderr is empty.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
