# Reproduction Trajectory — Bug 691: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6675](https://github.com/langchain-ai/langgraph/issues/6675)
- **Repository:** langchain-ai/langgraph @ `5212369bd0791806083f183cb19ccce024db8790`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the report and maintainer comments, which establish that the failure occurs in Pydantic's direct serialization of a `BaseMessage`-annotated state field.
2. Ran `bash setup_codebase.sh`. The reported minimal path is implemented by released `langchain-core` and Pydantic and does not import or execute LangGraph, so installed the issue-era `langchain-core==1.2.6` and `pydantic==2.12.5` in `.venv`.
3. Created one `AIMessage` containing a known `ToolCall`, then dumped it both directly and through `State(messages: list[BaseMessage])`.
4. Ran `bash run_repro.sh` and captured its expected nonzero result.

## Observed behavior

- Direct serialization retains the expected tool call: `{'name': 'quux', 'args': {'baz': 'qux'}, 'id': 'bar', 'type': 'tool_call'}`.
- The nested state serialization instead produced `{'content': 'foo', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': None}`, which has no `tool_calls` key.
- The final run printed `BUG REPRODUCED: State.model_dump() dropped AIMessage.tool_calls` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
