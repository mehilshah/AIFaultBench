# Reproduction Trajectory — Bug 754: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/20790](https://github.com/run-llama/llama_index/issues/20790)
- **Repository:** run-llama/llama_index @ `65ec78efddec0de3267a510b33108100faa053e4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout at `65ec78efddec0de3267a510b33108100faa053e4`.
2. Installed the pinned Python dependencies and the core, OpenAI, and OpenAI-like packages from that checkout into `.venv`.
3. Created an `OpenAILike` with `is_function_calling_model=False` and an injected local completion client that has no `tool_choice` argument.
4. Called `client.as_structured_llm(Invoice).complete(...)` through `bash run_repro.sh`.

## Observed behavior

- The invocation exited with status 1 after printing `OBSERVED BUG: Completions.create() got an unexpected keyword argument 'tool_choice'`.
- The injected client is local only; no LLM endpoint, API key, or provider network call is used.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
