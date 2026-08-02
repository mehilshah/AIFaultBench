# Bug 645

`ChatFireworks._combine_llm_outputs` incorrectly adds nested Fireworks token-usage dictionaries with `+=`. The offline repro supplies two recorded `prompt_tokens_details` payloads to the combiner and verifies that the pinned checkout raises the reported `TypeError`, with no provider client, credential, or network call.

Current result on this host: reproduced. `bash run_repro.sh` exits 1 and prints the observed nested-dictionary `TypeError`.

Files:

- `repro.py` — deterministic offline trigger.
- `requirements.txt` — pinned direct dependencies.
- `setup_env.sh` — creates the virtual environment and installs the checkout's Fireworks package.
- `run_repro.sh` — reproduction entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — final captured execution evidence.
- `reproduction.json` / `reproduction_trajectory.md` — structured and narrative evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
