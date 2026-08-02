# Bug 757

This issue reported a vLLM server 400 response being surfaced as
`AgentGenerationError` by smolagents. The deterministic repro replaces the
network client with a local fake that returns that exact upstream failure and
checks that the pinned checkout merely wraps it. The issue does not reproduce
as a smolagents fault on this host: maintainers identified the originating bug
as vLLM issue vllm-project/vllm#23318.

Files: `repro.py` is the no-network probe; `requirements.txt` declares that no
extra dependencies are needed; `setup_env.sh` creates the environment;
`run_repro.sh` is the entrypoint; `reproduction.json` and the two log files
record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
