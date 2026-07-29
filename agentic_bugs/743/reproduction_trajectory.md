# Reproduction Trajectory — Bug 743: autogen

- **Bug report:** [https://github.com/microsoft/autogen/issues/6788](https://github.com/microsoft/autogen/issues/6788)
- **Repository:** microsoft/autogen @ `9f2c5aa1be8f59ad830d253294ca84317f859b66`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the pinned `9f2c5aa1be8f59ad830d253294ca84317f859b66` commit.
2. Created `.venv` with the issue-era pinned dependencies and installed the checkout's `autogen-core` and `autogen-ext[openai]` packages editable.
3. Ran `bash run_repro.sh`. The script transforms an `AssistantMessage` containing two `FunctionCall` values, then submits the result to an in-process strict OpenAI-compatible endpoint stub; no provider or network call is made.

## Observed behavior

- The pinned transformer produced an assistant tool-call message with `role` and `tool_calls`, but no `content` key.
- The strict endpoint rejected the message at `['body', 'messages', 2, 'content']` with `openai.UnprocessableEntityError: Error code: 422`.
- `run_repro.sh` exited with status 1, as expected while the bug is present.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
