# Reproduction Trajectory — Bug 750: langgraph

- **Bug report:** [https://github.com/langchain-ai/langgraph/issues/6559](https://github.com/langchain-ai/langgraph/issues/6559)
- **Repository:** langchain-ai/langgraph @ `6c6978918e48cc41792ebcd0402e4358bfc12a31`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; on this machine Git created an empty repository, even though the pinned SHA was reachable through GitHub's commit API.
2. Retrieved the pinned source archive to inspect its package metadata, which identifies the snapshot as released `langgraph==1.0.4`; used that permitted released-package fallback and pinned the issue-era dependencies.
3. Compiled a `StateGraph` with no compile-time checkpointer, then supplied `InMemorySaver` only through `configurable[CONFIG_KEY_CHECKPOINTER]` to emulate runtime injection.
4. Ran the graph to its interrupt and resumed with `Command(resume="approved")`, while a deterministic `@task` call counter recorded whether the pre-interrupt task was replayed.

## Observed behavior

- The graph interrupted on its first invocation and resumed to `{'value': 'task-result', 'response': 'approved'}`.
- The completed pre-interrupt `@task` had `calls=1` after resume, rather than running twice.
- The final run printed `NOT_REPRODUCED: runtime-injected checkpointer cached @task output (calls=1)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

With `langgraph==1.0.4` and the issue-era dependency set, the runtime-injected `InMemorySaver` is used to restore task writes. The completed `@task` result is therefore cached across the interrupt/resume boundary, contradicting the reported re-execution behavior.
