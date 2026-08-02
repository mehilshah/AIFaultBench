# Bug 723

This bundle reproduces the legacy SSE transport forwarding an `httpx.ReadTimeout` after an MCP
session has initialized. It uses a fully in-memory HTTPX transport: no MCP server, model provider,
API key, or network connection is involved.

The fault reproduces on this host at `c92bb2f7ffaa61813d7cc350887f4ece38307769`.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` pins dependencies;
`setup_env.sh` creates the environment; `run_repro.sh` is the entrypoint; and the two log files
capture the final execution.

Run with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
