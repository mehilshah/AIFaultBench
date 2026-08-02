# Bug 652

At the pinned DSPy commit, `UsageTracker` tries to add two structured Anthropic
prompt-cache detail objects. `repro.py` feeds the real tracker two local Pydantic
stand-ins and verifies it raises the reported `TypeError`, without calling an LLM
provider or requiring credentials. The bug reproduces on this host.

Files: `repro.py` is the deterministic trigger; `requirements.txt` pins the
environment; `setup_env.sh` creates it; `run_repro.sh` is the entrypoint; and the
two log files record the final run. `reproduction.json` and
`reproduction_trajectory.md` contain the evidence and procedure.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
