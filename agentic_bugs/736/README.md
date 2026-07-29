# Bug 736

SWE-agent passed `pathlib.Path("/root/state.json")` to a POSIX container runtime. On Windows that serializes with backslashes, so the existing state file cannot be read and the agent receives an empty state. The repro uses a local fake container and Windows path semantics; it performs no model or network calls.

Current result on this host: reproduced. The script prints the backslash path and exits non-zero with a targeted assertion when the buggy code is present.

Files:

- `repro.py` — deterministic reproduction script.
- `requirements.txt`, `setup_env.sh`, and `run_repro.sh` — isolated environment and entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — output from the final run.
- `reproduction.json` and `reproduction_trajectory.md` — structured evidence and narrative.

Run it with:

```bash
bash run_repro.sh
```
