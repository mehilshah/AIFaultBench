# Bug 692

`langgraph-api==0.6.20` requires the keyword-only `is_for_execution` argument
on `get_graph`, while `langgraph-runtime-inmem==0.21.0` omits it from the
thread-history path. The offline repro stubs persistence only, executes that
real path, and checks for the reported `TypeError`. It reproduces on this host.

Files: `repro.py` is the minimal repro; `requirements.txt` pins the issue-era
released packages; `setup_env.sh` creates the environment; `run_repro.sh` is
the entrypoint; the log and trajectory files record the observed result.

Run:

```bash
bash run_repro.sh
```
