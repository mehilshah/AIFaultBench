# Reproduction Trajectory — Bug 765: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6439](https://github.com/langchain-ai/langgraph/issues/6439)
- **Repository:** langchain-ai/langgraph @ `0d4ac836e3a943a6a807910001f84a1d11b52776`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then verified the generated checkout at the pinned commit.
2. Created `.venv`, installed the pinned dependency set, and installed `codebase/libs/langgraph` editable.
3. Built a graph with separate `a -> f` and `d -> f` edges, where `d` can only run through `b -> c -> d`.
4. Invoked the graph with `done_d=False`; `f` raises if the required `d` update is not present.
5. Ran `bash run_repro.sh` and captured its non-zero final execution.

## Observed behavior

- `repro_stdout.log` reports `OBSERVED EARLY EXECUTION: node_f ran before node_d completed`.
- The final run exited with status 1, and `repro_stderr.log` ends in `RuntimeError: node_f ran before node_d completed`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
