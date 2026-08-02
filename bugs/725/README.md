# Bug 725

CrewAI's guardrail retry path mishandles a task configured with `output_pydantic`: after a guardrail failure, it passes the regenerated Pydantic object directly to `TaskOutput.raw`, despite that field requiring a string. `repro.py` uses a deterministic offline agent double and asserts the resulting `ValidationError`; it makes no LLM or provider request. The bug reproduced on this host with `crewai==1.14.2`, the version declared by the pinned commit. The checkout clone repeatedly terminated before checkout here, so the matching released package is used instead.

Files:

- `repro.py` — minimal deterministic offline reproduction.
- `requirements.txt` — pinned package dependency.
- `setup_env.sh` and `run_repro.sh` — environment setup and one-command runner.
- `repro_stdout.log` and `repro_stderr.log` — captured final run.
- `reproduction.json` and `reproduction_trajectory.md` — machine-readable and narrative evidence.

Run with:

```bash
bash run_repro.sh
```
