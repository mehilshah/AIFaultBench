# Reproduction Trajectory — Bug 668: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6771](https://github.com/pydantic/pydantic-ai/issues/6771)
- **Repository:** pydantic/pydantic-ai @ `e9ebd28626152401b9b485337ce6c1175dbbe681`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the pinned checkout revision.
2. Created `.venv`, installed the exact dependencies including `google-genai==1.74.0`, and installed the two local Pydantic AI packages in editable mode.
3. Ran `bash run_repro.sh`. The script uses an offline Google Cloud-shaped provider, asks `GoogleModel` for the configuration for a Gemini 3.5 model with a function tool and `WebFetchTool`, then passes that generated configuration to the installed SDK's real Vertex converter.

## Observed behavior

- `GoogleModel` set `include_server_side_tool_invocations=True`; `_ToolConfig_to_vertex` then raised `ValueError: include_server_side_tool_invocations parameter is not supported in Gemini Enterprise Agent Platform.`
- The final reproduction command exited with status 1 and made no HTTP or provider API request.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
