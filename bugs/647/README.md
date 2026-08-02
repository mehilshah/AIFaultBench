# Bug 647

`langgraph-cli` 0.4.29 allowed an incompatible pair of in-memory server
dependencies: `langgraph-runtime-inmem` 0.31.0.dev9 reads
`langgraph_api.config.LSD_PROM_METRICS_ENABLED`, which is absent from
`langgraph-api` 0.12.0.dev3. The offline repro enters the real runtime
lifespan after stubbing only its preceding service-startup functions and checks
for that exact `AttributeError`. It reproduces on this host (exit status 1 is
the intentional faulty-behavior verdict).

Files:

- `repro.py` — deterministic offline fault trigger.
- `requirements.txt` — issue-era incompatible package versions.
- `setup_env.sh` / `run_repro.sh` — environment setup and one-command runner.
- `repro_stdout.log` / `repro_stderr.log` — output from the final run.
- `reproduction.json` / `reproduction_trajectory.md` — structured evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
