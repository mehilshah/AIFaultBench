# Bug 766

At LangGraph 1.0.3, `CompiledStateGraph` is defined in `langgraph.graph.state` but is not re-exported by `langgraph.graph`. The reproduction checks that the report's exact public import raises the expected `ImportError`; on this host, the fault is reproduced.

Files: `repro.py` contains the assertion, `requirements.txt` pins the runtime dependencies, `setup_env.sh` creates the local install, `run_repro.sh` is the entrypoint, and `repro_stdout.log`/`repro_stderr.log` capture the final result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
