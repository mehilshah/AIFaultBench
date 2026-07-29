# Reproduction Trajectory — Bug 672: agno

- **Bug report:** [https://github.com/agno-agi/agno/issues/8644](https://github.com/agno-agi/agno/issues/8644)
- **Repository:** agno-agi/agno @ `eca49700e3d7e9ef78840abc6c15bbf5dca3f9e2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out the supplied pinned Agno revision.
2. Created `.venv`, installed the checkout's pinned runtime dependencies, and installed `codebase/libs/agno` editable.
3. Constructed an offline `AsyncBaseDb` fake with an `async get_session()` that returns a stored `WorkflowSession`; no database, model, API key, or network call is used by the repro.
4. Confirmed `Workflow.aget_session()` awaits that backend and returns the stored session, then called `Workflow.get_session()` against the same backend.

## Observed behavior

- `run_repro.sh` exited with status 1.
- `Workflow.get_session()` returned `None` even though its async counterpart loaded the stored session.
- Python emitted `RuntimeWarning: coroutine 'get_session' was never awaited`, proving the synchronous helper invoked the async database method without awaiting it.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
