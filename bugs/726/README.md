# Bug 726

At the pinned buggy commit, `AgentOutputSchema(dict[str, int], strict_json_schema=False)` treats the generic dictionary as a non-object output and wraps it under `response`. The repro verifies that the natural `{"a": 1}` payload fails while `{"response": {"a": 1}}` succeeds, then exits non-zero to signal the present bug. This reproduced on this host without an LLM, API key, or runtime network call.

Files: `repro.py` is the assertion-based reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` build and run the isolated environment; `repro_stdout.log` and `repro_stderr.log` contain the captured final run; `reproduction.json` and `reproduction_trajectory.md` record the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
