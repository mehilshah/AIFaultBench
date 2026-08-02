# Reproduction Trajectory — Bug 720: browser-use

- **Bug report:** [https://github.com/browser-use/browser-use/issues/4510](https://github.com/browser-use/browser-use/issues/4510)
- **Repository:** browser-use/browser-use @ `a1870b8b969553c375755c77d5d1cebf477c51f6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the pinned commit.
2. Created `.venv` with `bash setup_env.sh`, installing the editable checkout and its exact project-pinned dependencies.
3. Implemented an in-process Anthropic client stub that returns a real SDK `Message` with a `tool_use` block whose `action` field is a JSON string containing a literal newline in `done.text`.
4. Ran `bash run_repro.sh`; no provider, browser, or external runtime request was made.

## Observed behavior

- `run_repro.sh` exited with status 1 after printing `BUG REPRODUCED: nested newline action string was rejected as not a list`.
- The pinned parser raised `pydantic_core.ValidationError`: `Input should be a valid list [type=list_type]`, because `action` remained the string `[{"done":{"text":"first line\nsecond line"}}]`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
