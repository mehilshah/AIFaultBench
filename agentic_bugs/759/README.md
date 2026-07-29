# Bug 759

`VercelAIAdapter` with its default server-managed system prompt rebuilds the first inbound user request before the new-message boundary is calculated. Consequently, `new_messages()` includes that request on the first UI turn but not on a follow-up turn. The offline `TestModel` repro checks both turns and exits with the targeted assertion when the first-turn leak is present; it reproduced on this host.

Files: `repro.py` is the executable test, `requirements.txt` pins its dependencies, `setup_env.sh` creates the isolated environment, `run_repro.sh` is the entrypoint, and `repro_stdout.log` / `repro_stderr.log` are final-run evidence. `reproduction.json` and `reproduction_trajectory.md` record the verdict and steps.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
