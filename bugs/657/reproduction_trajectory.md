# Reproduction Trajectory — Bug 657: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/39100](https://github.com/langchain-ai/langchain/issues/39100)
- **Repository:** langchain-ai/langchain @ `73160209c3e60a8311f6e3402686d8982d735f83`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, which cloned the repository and checked out the pinned commit.
2. Created `.venv`, installed the pinned runtime dependencies, and installed the checkout's `langchain-core` and `langchain-anthropic` distributions editable.
3. Built a `SystemMessage` from `create_text_block()` and invoked `ChatAnthropic` with a local fake client in place of the Anthropic SDK client.
4. The fake client inspected the actual request passed through `ChatAnthropic.invoke` and rejected the leaked `id` field, without any network request.

## Observed behavior

- `run_repro.sh` exited with status 1 and printed `BUG REPRODUCED: unsupported id leaked into system.0`.
- The invocation reached `ChatAnthropic._create`; the local schema validator raised `AssertionError: Anthropic would reject this payload: system.0.id: Extra inputs are not permitted`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
