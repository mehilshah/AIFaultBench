# Bug 741

`phoenix.otel.settings.parse_env_headers()` in the issue-era
`arize-phoenix-otel==0.16.0` release crashes when one comma-delimited header
segment has no `=`. The reproduction calls it with `x=a,bad` and verifies the
specific unpacking `ValueError`. It reproduced on this host without any model
provider, API key, or runtime network call.

Files:

- `repro.py` — deterministic parser reproduction.
- `requirements.txt` — the released issue-era package pin.
- `setup_env.sh` / `run_repro.sh` — environment setup and single entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — captured final-run evidence.
- `reproduction.json` / `reproduction_trajectory.md` — structured and narrative evidence.

Run:

```bash
bash run_repro.sh
```
