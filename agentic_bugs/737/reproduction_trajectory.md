# Reproduction Trajectory — Bug 737: python-sdk

- **Bug report:** [https://github.com/modelcontextprotocol/python-sdk/issues/1967](https://github.com/modelcontextprotocol/python-sdk/issues/1967)
- **Repository:** modelcontextprotocol/python-sdk @ `b38716e5e3761dd2d52809d2d68ce65325faad5e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to clone the pinned buggy checkout.
2. Created an isolated `.venv`, installed the exact runtime dependency pins, and installed `codebase/` in editable mode.
3. Used `StreamableHTTPServerTransport.connect()` to create the transport memory streams, then called `terminate()` to model the DELETE shutdown path.
4. Sent a server log notification through `ServerSession.send_log_message()` after termination.

## Observed behavior

- The final run exited with status 1 and printed `BUG REPRODUCED: send_log_message after terminate raised anyio.ClosedResourceError`.
- `terminate()` closes the transport write stream; the subsequent logging send raises `anyio.ClosedResourceError` on the pinned implementation.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
