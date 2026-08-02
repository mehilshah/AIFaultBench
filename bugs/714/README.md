# Bug 714

This reproduction shows that the pinned Langflow checkout crashes when an offline graph step reaches a frozen vertex. With no chat/cache service, the fallback cache coroutine returns `None`, and `Graph.build_vertex` attempts to subscript it as cached vertex data. The repro uses a minimal in-memory graph and a patched service lookup, so it makes no provider or network calls. On this host it reproduces the reported `TypeError: 'NoneType' object is not subscriptable`.

Files:

- `repro.py` — minimal deterministic offline reproduction.
- `requirements.txt` — pinned dependency used to provide LFX's dependencies.
- `setup_env.sh` — creates the virtual environment and installs the pinned checkout.
- `run_repro.sh` — reproduction entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — final captured evidence.
- `reproduction.json` and `reproduction_trajectory.md` — structured result and narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
