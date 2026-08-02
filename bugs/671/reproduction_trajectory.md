# Reproduction Trajectory — Bug 671: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6331](https://github.com/pydantic/pydantic-ai/issues/6331)
- **Repository:** pydantic/pydantic-ai @ `77f86fa06f5fdde847f782710c5964e41037f096`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase` was at commit `77f86fa06f5fdde847f782710c5964e41037f096`.
2. Created `.venv`, installed the exact pinned third-party runtime dependencies, and installed the local root, slim, and graph packages editable.
3. Ran `repro.py` through `bash run_repro.sh`. It creates a `TestModel` agent, supplies an MCP tool from a dynamic capability function, and enables `override(native_tools=[CodeExecutionTool()])`.
4. The script catches TestModel's expected unsupported-built-in-tools error, then inspects the model request parameters it recorded and fails if the dynamic MCP tool was dropped.

## Observed behavior

- The final run printed `OBSERVED BUG: override request dropped dynamic MCPServerTool(id="dyn").`.
- The assertion showed the request native tools were `[CodeExecutionTool(kind='code_execution', optional=False, files=None)]`; `MCPServerTool(id='dyn', ...)` was missing.
- `run_repro.sh` exited with status 1 because the specific buggy behavior was observed. No network or provider API call was made.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
