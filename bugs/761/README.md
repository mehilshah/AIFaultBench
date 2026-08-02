# Bug 761

At the pinned Pydantic AI commit, a `RetryPromptPart` accepting a partial error-details dictionary can serialize successfully but cannot be deserialized through `ModelMessagesTypeAdapter`: the reload requires the omitted `input` key. The deterministic repro performs only local serialization and validation; it does not create a model client or make a provider request. On this host it reproduces the validation failure and exits with status 1.

Files: `repro.py` is the fault trigger, `requirements.txt` pins the runtime dependencies, `setup_env.sh` builds the isolated environment, `run_repro.sh` is the entrypoint, and `repro_stdout.log` / `repro_stderr.log` contain the final-run evidence. `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
