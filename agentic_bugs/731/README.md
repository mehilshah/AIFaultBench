# Bug 731

CAMEL's Minimax backend defaults to the mainland-China `api.minimaxi.com`
endpoint when `MINIMAX_API_BASE_URL` is absent, while international keys need
`api.minimax.io`. The offline repro constructs the reported model with inert
clients and checks the selected URL; it fails on this host with the incorrect
default and makes no provider request.

The issue-era release `camel-ai==0.2.90` is used because cloning the repository
was impractically large on the reference machine (the clone remained incomplete
after transferring over 140 MB). This is the public release immediately before
the issue's reported `0.2.91a4` build and contains the same faulty constructor
default.

Files:

- `repro.py` — deterministic offline reproducer.
- `requirements.txt` — pinned issue-era package.
- `setup_env.sh` — environment bootstrap.
- `run_repro.sh` — single reproduction entrypoint.
- `reproduction.json` and `reproduction_trajectory.md` — evidence and steps.

Run:

```bash
bash run_repro.sh
```
