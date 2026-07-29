# Bug 739

Phoenix's ATIF validator accepts a string in an agent step's `metrics` field. The
converter subsequently assumes that value is a mapping and raises `AttributeError`
when it calls `.get()`. This reproduction exercises the local validator and
converter only; it makes no provider or network calls at run time. On this host,
the pinned checkout reproduces the reported fault.

Files:

- `repro.py` — deterministic fault trigger.
- `requirements.txt` — exact pinned dependencies.
- `setup_env.sh` — isolated-environment setup.
- `run_repro.sh` — self-bootstrapping reproduction entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — captured final-run evidence.
- `reproduction.json` and `reproduction_trajectory.md` — machine-readable and narrative results.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
