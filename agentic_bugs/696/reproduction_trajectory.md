# Reproduction Trajectory — Bug 696: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/20973](https://github.com/run-llama/llama_index/issues/20973)
- **Repository:** run-llama/llama_index @ `9542621aec4ff90602806525f024a0f5812c5054`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the monorepo clone was impractically slow on the reference machine, so used the released `llama-index-core==0.14.15` specified by the issue.
2. Created `.venv` and installed the pinned package with `bash setup_env.sh`.
3. Used a local `DummyRetriever` and a `TrackingPostprocessor`, then called `ContextChatEngine._aget_nodes("test")`. The fake LLM is never called.
4. Ran `bash run_repro.sh` and captured its output.

## Observed behavior

- The final run exited with code `1` and printed `OBSERVED BUG: async path called_sync=True called_async=False`.
- It raised `AssertionError: sync postprocessor was called in async path`, proving `_aget_nodes()` used `postprocess_nodes()` instead of awaiting `apostprocess_nodes()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
