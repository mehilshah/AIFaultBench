# Bug 744

This reproduces AutoGen GraphFlow issue #6551 at the pinned 0.5.7 checkout. Local scripted agents take the conditional B -> D branch while C -> E and D -> E are both present; the scheduler wrongly leaves E blocked by the unchosen C branch and raises `RuntimeError: No available speakers found.` No model provider, API key, or network call is used while reproducing.

The fault reproduced on this host: `run_repro.sh` exits 1 after printing the observed RuntimeError.

Files:

- `repro.py` — deterministic no-network reproduction.
- `requirements.txt` and `setup_env.sh` — isolated environment setup.
- `run_repro.sh` — one-command reproduction entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — output from the final run.
- `reproduction.json` and `reproduction_trajectory.md` — machine-readable and narrative evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
