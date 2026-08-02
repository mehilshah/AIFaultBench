# Reproduction Trajectory — Bug 722: python-sdk

- **Bug report:** [https://github.com/modelcontextprotocol/python-sdk/issues/2704](https://github.com/modelcontextprotocol/python-sdk/issues/2704)
- **Repository:** modelcontextprotocol/python-sdk @ `3eb579948a4719d606d2adbd1f3f69371c9c0f48`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and confirmed the checkout was at the pinned commit.
2. Created `.venv` with `bash setup_env.sh`; the reproduction needs only the Python standard library.
3. Parsed and compiled the exact `basic_server_port` fixture from the pinned `tests/shared/test_streamable_http.py` without importing the test suite's unrelated dependencies.
4. Called that fixture, reserved the returned port with an intruder listener, and attempted the delayed server bind that the fixture's multiprocessing server would make.
5. Ran `bash run_repro.sh` and captured its final output.

## Observed behavior

- The fixture returned port `46133` after closing the socket that had selected it.
- The intruder listener successfully acquired that port, and the delayed server bind failed with `EADDRINUSE`.
- `run_repro.sh` printed `BUG REPRODUCED: basic_server_port released 46133; delayed server bind raised EADDRINUSE` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
