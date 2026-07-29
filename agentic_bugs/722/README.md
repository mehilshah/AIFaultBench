# Bug 722

`tests/shared/test_streamable_http.py` chooses a free TCP port and closes the
selecting socket before its server process binds that port. Another parallel
test worker can reserve the released port in that interval, causing the
intended server to fail with `EADDRINUSE` or clients to reach the wrong server.
The repro invokes the exact pinned fixture and deterministically demonstrates
that delayed-bind failure. It reproduced on this host.

Files:

- `repro.py` — deterministic reproduction script
- `requirements.txt` — dependency declaration (standard library only)
- `setup_env.sh` — isolated environment setup
- `run_repro.sh` — reproduction entrypoint
- `repro_stdout.log` / `repro_stderr.log` — final captured output
- `reproduction.json` — machine-readable verdict
- `reproduction_trajectory.md` — detailed reproduction record

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
