# Reproduction Trajectory — Bug 753: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/20851](https://github.com/run-llama/llama_index/issues/20851)
- **Repository:** run-llama/llama_index @ `a771a4f67e43bb5d2675972496a4e5c70f847052`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase` was checked out at the pinned commit.
2. Created `.venv`, installed the exact dependency pins, and installed the checkout's core and Bedrock Converse packages editable.
3. Replaced the Bedrock request function with a recorded local stream containing a reasoning text delta followed by a signature-only `reasoningContent` delta.
4. Consumed `BedrockConverse.stream_chat` and asserted that its resulting `ThinkingBlock` retained that signature.

## Observed behavior

- The final `ThinkingBlock` had `additional_information["signature"] == ""` instead of `"signature-from-signature-only-delta"`.
- `repro.py` printed `BUG OBSERVED: signature-only delta was dropped (expected 'signature-from-signature-only-delta', got '')` and raised `AssertionError: Bedrock Converse lost a signature-only reasoning delta`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
