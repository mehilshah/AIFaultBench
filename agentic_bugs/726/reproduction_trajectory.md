# Reproduction Trajectory — Bug 726: openai-agents-python

- **Bug report:** [https://github.com/openai/openai-agents-python/issues/3315](https://github.com/openai/openai-agents-python/issues/3315)
- **Repository:** openai/openai-agents-python @ `bc3607bae44d9d56c7ae0e40323d0b4a560aa254`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the issue report and confirmed that it exercises local `AgentOutputSchema` logic only, with no model invocation.
2. Ran `bash setup_codebase.sh`; its clone left an empty generated Git repository, so fetched the specified pinned commit into that repository and checked it out.
3. Created `.venv`, installed the pinned dependencies and the pinned checkout in editable mode.
4. Ran `bash run_repro.sh`, which creates schemas for `dict` and `dict[str, int]`, validates both relevant JSON shapes, and exits 1 when the reported faulty behavior is observed.

## Observed behavior

- Bare `dict` was unwrapped, while `dict[str, int]` was wrapped under the `response` property.
- The natural payload `{"a": 1}` raised `ModelBehaviorError` with `response` reported as a required missing field; `{"response": {"a": 1}}` validated to `{'a': 1}`.
- The final run printed `BUG REPRODUCED: dict[str, int] requires an unwanted response wrapper` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
