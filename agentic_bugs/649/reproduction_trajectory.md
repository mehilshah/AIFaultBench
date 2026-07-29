# Reproduction Trajectory — Bug 649: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/21422](https://github.com/run-llama/llama_index/issues/21422)
- **Repository:** run-llama/llama_index @ `33f7ba4e3c5e20c6b1a26cae354fa39900e6ffb4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out the supplied pinned revision (the initial clone transfer left no refs, so the same remote was fetched at the specified commit to complete the generated checkout).
2. Created `.venv`, installed the exact runtime dependency pins, and installed `codebase/llama-index-core` in editable mode.
3. Built a local `ChatResponse` whose `raw` field holds a Pydantic `StructuredReply`; no LLM client, API key, or external service was used.
4. Called `LLMChatEndEvent(messages=[], response=response).model_dump()` and then checked the caller-owned `response.raw` value.
5. Ran `bash run_repro.sh` for the final captured result.

## Observed behavior

- The final run printed `BUG REPRODUCED: LLMChatEndEvent.model_dump changed ChatResponse.raw to dict`.
- It then raised `RuntimeError: ChatResponse.raw was mutated in place during event serialization` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
