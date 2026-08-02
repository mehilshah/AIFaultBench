# Bug 690

Setting `LANGGRAPH_RUNTIME_EDITION=postgres` makes the LangGraph API runtime selector look for the unpublished `langgraph_runtime_postgres` module. The repro installs the issue-era public API package, sets that edition, and verifies that the selector raises the reported `ImportError` without making any network or model calls. On this host the fault reproduced: `run_repro.sh` exits 1 after printing the precise missing-backend error.

The source-clone setup was started as requested, but its full-clone pack had reached 331 MiB without a checkout; this entry therefore uses the issue-era released `langgraph-api==0.7.6` package, which contains the exact runtime selector named in the report.

Files:

- `repro.py` — minimal deterministic import reproduction.
- `requirements.txt` — issue-era released API dependency.
- `setup_env.sh` — creates the isolated environment.
- `run_repro.sh` — one-command reproduction entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — captured final-run evidence.
- `reproduction.json` / `reproduction_trajectory.md` — structured result and narrative.

Run with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
