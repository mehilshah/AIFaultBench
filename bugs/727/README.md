# Bug 727

On Windows, the pinned SDK constructs the executable path for a Linux sandbox helper with host-native `pathlib.Path`. This converts `/tmp/openai-agents/bin/...` to `\tmp\openai-agents\bin\...`; the Linux sandbox therefore cannot find it and startup is wrapped as `WorkspaceStartError`. The reproduction drives the pinned path-validation method using Windows path semantics and a no-network recording sandbox, then asserts the malformed executable path and exits non-zero. It reproduced on this host.

Files:

- `repro.py` — deterministic no-network reproduction.
- `requirements.txt` — exact environment dependency pins.
- `setup_env.sh` and `run_repro.sh` — environment setup and entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — final captured execution evidence.
- `reproduction.json` and `reproduction_trajectory.md` — structured and narrative results.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
