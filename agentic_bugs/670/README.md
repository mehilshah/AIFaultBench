# Bug 670

On the pinned pydantic-ai checkout, the shared dataclass `repr` helper compares every field with its default. A required `ToolReturnPart.content` whose `__ne__` result cannot be coerced to `bool` makes both `ToolReturnPart` and enclosing `ModelRequest` formatting raise `ValueError`. The deterministic repro uses a tiny local array-like stand-in, not NumPy or any model/provider API, and reproduces the failure on this host.

Files:

- `repro.py` — deterministic failing script.
- `requirements.txt` and `setup_env.sh` — isolated, pinned environment setup.
- `run_repro.sh` — bootstrap-and-run entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — final captured evidence.
- `reproduction.json` and `reproduction_trajectory.md` — result metadata and narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
