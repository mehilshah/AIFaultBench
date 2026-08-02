# Reproduction Trajectory — Bug 749: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6576](https://github.com/langchain-ai/langgraph/issues/6576)
- **Repository:** langchain-ai/langgraph @ `df191731918482c5eaf2934a2df0c9cb3571db0c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout at the requested pinned commit.
2. Created `.venv`, installed `langchain-core==1.1.0`, and installed the relevant LangGraph libraries editable from the pinned checkout.
3. Defined a `@tool` function that requires `runtime: ToolRuntime` and invoked it with `{}`, mirroring the reported custom node's `tool.invoke(tool_call["args"])` call.

## Observed behavior

- The final `bash run_repro.sh` exited with status 1.
- stdout contained `OBSERVED: ValidationError: runtime Field required`.
- Pydantic reported `runtime` as a required missing field for `get_greeting_rules`, with `input_value={}`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
