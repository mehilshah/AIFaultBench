# Reproduction Trajectory — Bug 665: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/21378](https://github.com/run-llama/llama_index/issues/21378)
- **Repository:** run-llama/llama_index @ `91fe33e75ce31d3ca447c017a5ea153ed8b38700`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the full repository transfer was impractically large on this host, so installed the released issue-era packages `llama-index-core==0.14.8` and `llama-index-llms-openai==0.7.5` instead.
2. Created an assistant `ChatMessage` with a `ToolCallBlock` whose `tool_kwargs` is `{"agent_name": "worker"}`.
3. Passed the message directly to `to_openai_message_dict`, with no LLM client or provider request.
4. Ran `bash run_repro.sh`, which asserts that OpenAI Chat Completions arguments must be a string and deliberately fails when the buggy dictionary is emitted.

## Observed behavior

- The converter produced `function.arguments` as `dict: {'agent_name': 'worker'}` rather than a JSON string.
- The final run exited 1 with `AssertionError: OpenAI Chat Completions requires function.arguments to be a JSON string`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
