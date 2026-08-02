# Reproduction Trajectory — Bug 767: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6370](https://github.com/langchain-ai/langgraph/issues/6370)
- **Repository:** langchain-ai/langgraph @ `a6dde39be72e0a8f7ea3eea946e0993720e982ce`
- **Outcome:** Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that the checkout resolved to the pinned commit.
2. Created `.venv` with the pinned dependencies and installed `codebase/libs/langgraph` editable.
3. Built the report's `StateGraph` with a conditional edge returning three `Send` objects. The mapped node encodes its received runtime value into its result.
4. Ran the graph with `context={"my_runtime_value": "ctx"}` and then without context, capturing the final `bash run_repro.sh` output.

## Observed behavior

- With context supplied, all three mapped nodes returned values containing `ctx` (`ctx:lions`, `ctx:elephants`, and `ctx:penguins`).
- Without context, the mapped node raised the report's exact `RuntimeError: Runtime context is not available`; this is expected for an invocation that omits context.
- The final command exited 0 and printed `NOT_REPRODUCED: Send-mapped nodes received supplied Runtime context; the reported RuntimeError occurs only when context is omitted.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The issue was closed after the reporter found that LangGraph Studio resumed an interrupted SDK run without re-supplying its context, causing the intentional `None` context observed by the node. At the pinned checkout, a `Send`-mapped node receives a supplied `Runtime` context, so the alleged propagation failure is not an executable product bug.
