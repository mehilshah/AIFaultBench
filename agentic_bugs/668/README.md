# Bug 668

At the pinned pydantic-ai revision, a Gemini 3+ `GoogleModel` unconditionally enables `include_server_side_tool_invocations` when a native web-fetch tool is present. The offline reproduction checks that the real Vertex converter in `google-genai==1.74.0` rejects that generated configuration with the reported `ValueError`, before any API request. Result on this host: reproduced.

Files: `repro.py` is the reproducer; `requirements.txt` and `setup_env.sh` create its environment; `run_repro.sh` is the entrypoint; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the verdict.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
