# Reproduction Trajectory — Bug 762: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/5893](https://github.com/pydantic/pydantic-ai/issues/5893)
- **Repository:** pydantic/pydantic-ai @ `a6b2dbd68fa46287aa061f2dc726c9fd6cb870d2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and completed checkout of the pinned commit in `codebase/`.
2. Created `.venv`, installed `temporalio==1.27.2`, then installed the checkout's `pydantic_graph` and `pydantic_ai_slim[temporal]` packages in editable mode.
3. Constructed a `TemporalAgent` around an offline `TestModel` agent with a dataclass dependency type.
4. Asked Temporal for each decorated activity's cached `arg_types`, then ran the check through `bash run_repro.sh`.

## Observed behavior

- The non-streaming activity retained `typing.Any | None`, whereas the streaming activity captured `__main__.MyDeps | None`.
- The final `bash run_repro.sh` exited with status 1 and printed `BUG REPRODUCED: request captured typing.Any | None; stream captured __main__.MyDeps | None`.
- The repro creates no provider client and makes no runtime network calls.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
