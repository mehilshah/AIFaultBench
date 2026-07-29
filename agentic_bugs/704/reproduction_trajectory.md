# Reproduction Trajectory — Bug 704: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6051](https://github.com/pydantic/pydantic-ai/issues/6051)
- **Repository:** pydantic/pydantic-ai @ `a84f2b31d14de3572d51676ea1839c031d85362a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the resulting detached checkout is `a84f2b31d14de3572d51676ea1839c031d85362a`.
2. Created an isolated environment with `google-genai==2.8.0` and installed `codebase/pydantic_ai_slim` editable, so the checker imports the pinned checkout.
3. Constructed `GoogleModel` with an offline dummy provider key, a profile enabling server-side tool invocations, one local function tool, and `CodeExecutionTool`.
4. Called only the local `_get_tool_config()` method, then ran `bash run_repro.sh` and captured its output.

## Observed behavior

- The tool configuration had `include_server_side_tool_invocations=None` despite containing both a function declaration and `CodeExecutionTool` with the capability profile enabled.
- `run_repro.sh` exited with status 1 and raised `AssertionError: GoogleModel omitted include_server_side_tool_invocations for CodeExecutionTool with function calling`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
