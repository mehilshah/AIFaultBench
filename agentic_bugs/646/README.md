# Bug 646

`ChatAnthropic` drops the required `thinking` field when an empty thinking block
is streamed as a start event followed only by a `signature_delta`. The offline
reproduction constructs that exact typed event sequence and verifies that the
resulting replay payload omits `thinking`, then fails deliberately to make the
buggy behavior unambiguous. The bug reproduced on this host at the pinned
commit; no API key or network model call is used.

Files:

- `repro.py` — deterministic failing reproduction.
- `requirements.txt` — pinned external dependencies.
- `setup_env.sh` — creates the virtual environment and installs checkout packages.
- `run_repro.sh` — bootstrap and reproduction entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — output from the final failing run.
- `reproduction.json` / `reproduction_trajectory.md` — benchmark evidence.

Run it with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
