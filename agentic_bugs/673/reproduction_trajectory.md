# Reproduction Trajectory — Bug 673: agno

- **Bug report:** [https://github.com/agno-agi/agno/issues/8235](https://github.com/agno-agi/agno/issues/8235)
- **Repository:** agno-agi/agno @ `1a32f1651b0427ed8c70aa6123a5a93610d8c3d0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then completed the checkout of the requested pinned revision when the initial clone had no checked-out HEAD.
2. Created `.venv`, installed the exact pinned dependencies, and installed `codebase/libs/agno` as the editable monorepo package.
3. Used an offline `OfflineTeam` double whose `arun(stream=True, stream_events=True)` async iterator yields a `TeamRunOutput` accumulator.
4. Passed that double to `team_response_streamer` and captured the final `bash run_repro.sh` execution.

## Observed behavior

- `TeamRunOutput` exposes `.events` but not `.event`.
- `team_response_streamer` passed it to `format_sse_event`, producing `AttributeError: 'TeamRunOutput' object has no attribute 'event'. Did you mean: 'events'?` at `agno/os/utils.py:199`.
- The router caught that exception and emitted a `TeamRunError` SSE response; `repro.py` recognized this precise error and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
