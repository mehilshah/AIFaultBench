# Bug 662

CrewAI 1.14.1 fails to register native MCP tools when discovery reaches a tool with a recursive JSON Schema. The offline reproduction supplies ten ordinary tools and one recursive-schema tool, then verifies that the resolver emits the issue's exact maximum-recursion-depth `RuntimeError`. This host reproduced the fault without an MCP server, LLM provider, API key, or runtime network access.

Files: `repro.py` is the deterministic reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` set up and execute it; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the verdict.

Run with:

```bash
bash run_repro.sh
```
