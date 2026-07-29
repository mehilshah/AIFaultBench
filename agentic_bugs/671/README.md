# Bug 671

When `Agent.override(native_tools=...)` is active, a native tool supplied by a
dynamic capability function is omitted from the model request. The offline
reproducer uses `TestModel`, which records the request without contacting an
LLM provider, and fails after confirming that the override's
`CodeExecutionTool` is present while the dynamic `MCPServerTool` is absent.
On this host, the bug is reproduced at the pinned commit.

Files:

- `repro.py` — deterministic offline reproduction
- `requirements.txt` — pinned third-party runtime dependencies
- `setup_env.sh` — creates the virtual environment and installs the checkout
- `run_repro.sh` — runs the reproduction
- `repro_stdout.log` / `repro_stderr.log` — output from the final run
- `reproduction.json` / `reproduction_trajectory.md` — recorded evidence

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
