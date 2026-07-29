# Bug 767

This bundle checks the claim that LangGraph `Send`-mapped nodes lose a supplied
`Runtime` context.  On this host the pinned checkout propagates the context to
all mapped nodes; the reported `RuntimeError` is observed only when the graph
is invoked without a context, matching the issue's closing comment about
resuming from Studio without resupplying it.

Result: not reproduced on the reference machine.

Files: `repro.py` contains the deterministic graph, `requirements.txt` pins its
dependencies, `setup_env.sh` builds the virtual environment, `run_repro.sh`
runs it, and `repro_stdout.log`/`repro_stderr.log` capture the final execution.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
