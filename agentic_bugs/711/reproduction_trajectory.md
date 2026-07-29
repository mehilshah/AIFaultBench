# Reproduction Trajectory — Bug 711: camel

- **Bug report:** [https://github.com/camel-ai/camel/issues/3339](https://github.com/camel-ai/camel/issues/3339)
- **Repository:** camel-ai/camel @ `adf4aba7f4cf1bf91c247b2b2c51ad11f5374ab2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout resolved to the pinned commit.
2. Created `.venv`, installed the checkout editable, and pinned `mcp==1.13.0`, whose `FastMCP` API is compatible with this issue-era CAMEL checkout.
3. Created a `ChatAgent` with CAMEL's local `StubModel` and a local async tool that always raises `RuntimeError("deterministic offline tool failure")`.
4. Invoked CAMEL's `_aexecute_tool_from_stream_data` helper with a fixed tool-call ID, then inspected its in-memory OpenAI messages.
5. Ran `bash run_repro.sh`; it exited 1 after the reproducer found a lone `tool` message with no preceding assistant `tool_calls` message.

## Observed behavior

- The deterministic local failure was stored in the tool result as `Error executing async tool 'fail_offline_tool': deterministic offline tool failure`.
- The only recorded message had `role: tool` and `tool_call_id: call_offline_failure`; the expected assistant tool-call message was absent.
- The reproducer printed `OBSERVED BUG: failed async tool left an unpaired tool message (tool_call_id=call_offline_failure)` and raised the targeted assertion.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
