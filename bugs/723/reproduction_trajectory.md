# Reproduction Trajectory — Bug 723: python-sdk

- **Bug report:** [https://github.com/modelcontextprotocol/python-sdk/issues/1708](https://github.com/modelcontextprotocol/python-sdk/issues/1708)
- **Repository:** modelcontextprotocol/python-sdk @ `c92bb2f7ffaa61813d7cc350887f4ece38307769`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, which cloned the repository and checked out the pinned commit.
2. Created `.venv`, installed the exact dependency pins in `requirements.txt`, and installed `codebase` editable.
3. Ran `repro.py`, which uses an in-memory HTTPX transport to deliver a valid SSE endpoint and MCP initialization response.
4. After `ClientSession.initialize()` completed, the transport deterministically raised `httpx.ReadTimeout`; the legacy SSE reader forwarded it into the session message handler.

## Observed behavior

- `run_repro.sh` exited with status 1 after the assertion deliberately marked the observed faulty behavior.
- The final stdout says `MCP session initialized using local stub` followed by `OBSERVED BUG: ReadTimeout: scripted silent SSE stream`.
- The final stderr trace shows `httpx.ReadTimeout` propagating from `codebase/src/mcp/client/sse.py`, line 73.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
