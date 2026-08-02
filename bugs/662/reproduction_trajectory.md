# Reproduction Trajectory — Bug 662: crewAI

- **Bug report:** [https://github.com/crewAIInc/crewAI/issues/5474](https://github.com/crewAIInc/crewAI/issues/5474)
- **Repository:** crewAIInc/crewAI @ `1c90d574abb9f28dd09de8ded437bcad19fa97dc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` twice. The full repository clone did not finish in the reference environment's execution window, so used the issue report's released package version, `crewai==1.14.1`.
2. Created `.venv` and installed the pinned release from `requirements.txt`.
3. Replaced `MCPClient` with an in-process fake that returns ten simple MCP tools and an eleventh tool whose JSON schema has a self-referential `$defs.Node` schema.
4. Ran `bash run_repro.sh`; the fake does not open sockets, spawn a process, call an LLM, or require credentials.

## Observed behavior

- `run_repro.sh` exited with status 1 after printing `OBSERVED BUG: Failed to get native MCP tools: maximum recursion depth exceeded`.
- The captured traceback shows `RecursionError: maximum recursion depth exceeded` in `force_additional_properties_false`, wrapped by `MCPToolResolver._resolve_native` as the reported `RuntimeError`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
