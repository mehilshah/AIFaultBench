# Reproduction Trajectory — Bug 751: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6456](https://github.com/langchain-ai/langgraph/issues/6456)
- **Repository:** langchain-ai/langgraph @ `df8becd5cfc74bb09ab2d7cbdf17c5559114b8d8`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read the issue report and comments, which identify `Send` values being JSON-encoded by an older Postgres checkpoint layout.
2. Ran `bash setup_codebase.sh` and confirmed that `codebase` was checked out at `df8becd5cfc74bb09ab2d7cbdf17c5559114b8d8`.
3. Created `.venv`, installed the pinned requirements, and installed the LangGraph, checkpoint, checkpoint-postgres, prebuilt, and SDK packages from the checkout in editable mode.
4. Ran the issue's map-reduce graph with dynamically returned `Send` objects. The repro subclassed `PostgresSaver` only to replace its database cursor with an in-process cursor that calls `json.dumps` on every `Jsonb` argument, avoiding a PostgreSQL server while exercising the real saver write path.
5. Captured the final `bash run_repro.sh` output.

## Observed behavior

- The final run exited with status 0.
- Stdout was `NOT REPRODUCED: PostgresSaver serialized Send tasks and completed the graph`.
- The graph returned all three expected joke values, showing that the `Send` branches executed.
- The JSONB-validating cursor did not raise `TypeError: Object of type Send is not JSON serializable`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The pinned LangGraph 1.0.3 checkout uses checkpoint format v4. Dynamic `Send` tasks are stored in the `TASKS` blob channel and serialized through the checkpointer serializer, rather than being included in the JSONB checkpoint record that psycopg encodes. Consequently the reported `TypeError` does not occur.
