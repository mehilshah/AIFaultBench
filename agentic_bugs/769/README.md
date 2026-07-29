# Bug 769

At the pinned smolagents commit, `@tool` builds invalid source for a function with a multiline signature. Calling `to_dict()`—the serialization path used before sending tools to a remote Python executor—then raises `SyntaxError`. The offline repro defines such a tool and asserts that exact failure; it makes no model or network calls.

Current result on this host: reproduced.

Files: `repro.py` (minimal trigger), `requirements.txt` (pinned runtime dependencies), `setup_env.sh` and `run_repro.sh` (environment and entrypoint), captured logs, `reproduction.json`, and `reproduction_trajectory.md`.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
