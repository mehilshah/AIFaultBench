# Reproduction Trajectory — Bug 664: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/21579](https://github.com/run-llama/llama_index/issues/21579)
- **Repository:** run-llama/llama_index @ `d601b0f36af4f6362375eefeda509d1070340652`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. Its clone did not complete on this host (only temporary Git packfiles were written), so used the published issue-era integration package `llama-index-llms-bedrock-converse==0.14.9` instead.
2. Created `.venv` and installed the exact package set in `requirements.txt`.
3. Replaced the adapter's in-process Bedrock request helper with a deterministic fake `ConverseStream` response containing one tool use whose JSON input arrives in two chunks.
4. Called `BedrockConverse.stream_chat` and inspected the final emitted `ToolCallBlock`.

## Observed behavior

- The final tool block had `tool_kwargs` equal to the raw string `{"document_id":"123"}`, rather than a dictionary.
- `repro.py` printed `OBSERVED BUG: ToolCallBlock.tool_kwargs is str: {"document_id":"123"}` and raised `AssertionError: streaming tool input was not normalized to a dict`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
