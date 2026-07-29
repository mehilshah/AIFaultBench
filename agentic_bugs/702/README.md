# Bug 702

`PydanticAIPlugin` does not pass `genai_prices` or `httpx2` through Temporal's
workflow sandbox. Calling `ModelResponse.cost()` then lazily imports that stack
inside a workflow and raises `RestrictedWorkflowAccessError` while `httpx2`
subclasses `urllib.request.Request`. The reproduction exercises that sandbox
path directly; it makes no LLM or network call. This host reproduces the fault.

Files: `repro.py` contains the deterministic reproducer; `requirements.txt`
pins its dependencies; `setup_env.sh` creates the environment and installs the
pinned checkout; `run_repro.sh` is the entry point; and the two log files record
the final run. `reproduction.json` is the machine-readable verdict and
`reproduction_trajectory.md` records the reproduction steps.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
