# Reproduction Trajectory — Bug 660: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6789](https://github.com/langchain-ai/langgraph/issues/6789)
- **Repository:** langchain-ai/langgraph @ `f9870bc9aefeb271927ffd5ad558b22e416793ef`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. On this host it created an empty Git repository despite a successful status, so GitHub's source archive for the identical pinned SHA was used to inspect and execute the source.
2. Created `.venv`, installed the exact runtime dependency pins, and installed `libs/checkpoint` and `libs/langgraph` editable from that source tree.
3. Ran `bash run_repro.sh` offline. It tests raw `ormsgpack`, LangGraph's serializer, the exact unsupported node-return structure from the report, and a supported checkpointed conditional-routing graph.

## Observed behavior

- Raw `ormsgpack` raised `TypeError: Type is not msgpack serializable: Send`.
- `JsonPlusSerializer` produced a `msgpack` payload and restored `Send(node='worker', arg={'task': 'alpha'})` exactly.
- The report's graph raised `InvalidUpdateError: Expected dict, got [Send(...)]`; the supported graph completed with `results=['alpha', 'beta']` under `InMemorySaver`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The pinned serializer contains a `SendProtocol` msgpack handler, so it serializes `Send`. The graph in the report uses an unsupported `list[Send]` return from a node; the valid forms are a conditional-edge return or `Command(goto=[Send(...)])`.
