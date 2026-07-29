# Bug 656

At the pinned browser-use 0.11.5 checkout, the sensitive-data instruction gives
only a generic `<secret>`-tag rule. When the model emits the literal
`user_name` action reported in the issue, the real action replacement path
leaves that literal unchanged instead of entering the configured value. The
reproduction uses a deterministic fake model action and makes no browser or
provider calls. On this host the fault reproduces (the script exits non-zero
after printing the observed literal placeholder).

Files:

- `repro.py` — deterministic reproduction script.
- `requirements.txt` — the pinned missing runtime dependency required by this checkout.
- `setup_env.sh` / `run_repro.sh` — environment setup and single entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — output from the final run.
- `reproduction.json` / `reproduction_trajectory.md` — structured and narrative evidence.

Run with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
