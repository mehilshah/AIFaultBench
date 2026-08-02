# Reproduction Trajectory — Bug 768: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6346](https://github.com/langchain-ai/langgraph/issues/6346)
- **Repository:** langchain-ai/langgraph @ `5796ca9a0ad8ec53dbcf12fa9f1d671b826e5f1d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. Its initial large clone transfer did not complete in the execution interface, so I fetched the pinned commit at depth 1, checked it out, and verified `5796ca9a0ad8ec53dbcf12fa9f1d671b826e5f1d`.
2. Installed the issue-era released component `langgraph-api==0.4.46` and `uvloop==0.21.0` in `.venv`. The report identifies this released package, whose UI-bundler source is not present in the public LangGraph checkout.
3. Ran `bash run_repro.sh`. The script imports the real `langgraph_api.js.ui` function, configures uvloop, and replaces `npx` with the local Python executable. No subprocess is started because uvloop raises at the faulty `env=os.environ` argument; no network, provider, or LLM call occurs.
4. Captured that final run's output in the required log files.

## Observed behavior

- `bash run_repro.sh` exited with status 1.
- stdout reported `OBSERVED BUG: TypeError: Expected dict, got _Environ`.
- The traceback reaches `langgraph_api/js/ui.py`, line 62, in `_start_ui_bundler_process`, then uvloop raises `TypeError: Expected dict, got _Environ`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
