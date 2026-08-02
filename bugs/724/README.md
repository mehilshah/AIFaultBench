# Bug 724

CrewAI 1.14.3 cannot JSON-serialize a `Task` containing a callable in its
`guardrails` field. Checkpointing uses the same `model_dump(mode="json")`
operation, so a checkpoint can fail even when the user state itself contains
only JSON-compatible data. The repro creates only local Agent, Crew, Task,
and guardrail objects; it makes no model or network call at runtime.

Current result on this host: reproduced on the pinned checkout.

Files: `repro.py`, `requirements.txt`, `setup_env.sh`, `run_repro.sh`,
`repro_stdout.log`, `repro_stderr.log`, `reproduction.json`, and
`reproduction_trajectory.md`.

Run with:

```bash
bash run_repro.sh
```
