# Bug 700

At the pinned smolagents commit, the core installation does not include the optional `ddgs` package. Constructing `DuckDuckGoSearchTool` therefore raises the reported `ImportError` before an agent can make any model or network call. The repro asserts the exact error and chained `ModuleNotFoundError`; on this host, the fault reproduces.

Files: `repro.py` is the deterministic repro; `requirements.txt` pins its dependencies; `setup_env.sh` creates the environment; `run_repro.sh` is the entrypoint; `repro_stdout.log` and `repro_stderr.log` contain the final captured execution; `reproduction.json` and `reproduction_trajectory.md` record the result. The original report and issue metadata are in `bug_report.txt` and `github.json`.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
