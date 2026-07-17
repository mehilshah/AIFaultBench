# Reproduction Trajectory — Bug 186: marimo

- **Bug report:** [https://github.com/marimo-team/marimo/issues/7898](https://github.com/marimo-team/marimo/issues/7898)
- **Repository:** marimo-team/marimo @ `88937c9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Installed the local codebase in an isolated virtual environment with `bash setup_env.sh`.
2. Started a minimal Marimo Starlette app with `base_url=/my/custom/path` and a mocked pylsp proxy.
3. Probed websocket handshakes with curl; the prefixed path was rejected and the root path upgraded successfully.

## Observed behavior

- In the local Marimo app with base_url=/my/custom/path, the LSP websocket upgrade to /my/custom/path/lsp/pylsp was rejected with HTTP/1.1 403 Forbidden, while the same handshake to /lsp/pylsp returned HTTP/1.1 101 Switching Protocols.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
