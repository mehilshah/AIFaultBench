# Reproduction Trajectory — Bug 703: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6081](https://github.com/pydantic/pydantic-ai/issues/6081)
- **Repository:** pydantic/pydantic-ai @ `1e8adad9155a3656bb037a844f238a408e6e95f5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase/` was checked out at the pinned buggy commit.
2. Created `.venv`, installed the pinned Bedrock dependencies, and installed the checkout's `pydantic_graph` and `pydantic_ai_slim` packages in editable mode.
3. Built the issue's completed tool-call history followed by an attachment-bearing `UserPromptPart`, then called `BedrockConverseModel._map_messages`. This uses an `s3://` document URL and only local conversion code, so it makes neither an AWS request nor an LLM call.
4. Ran `bash run_repro.sh`; the script deliberately raises after asserting the faulty message shape, making the entrypoint exit non-zero.

## Observed behavior

- The final Bedrock user message has content blocks `['toolResult', 'text', 'document']`.
- `repro.py` raises `RuntimeError: BUG REPRODUCED: Bedrock would reject toolResult and document in one user message` after observing that specific invalid co-location.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
