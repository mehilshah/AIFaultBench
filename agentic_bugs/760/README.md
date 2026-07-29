# Bug 760

`add_mapping_edge(..., downstream_join_id=...)` dispatches a join twice for a non-empty mapping. The first dispatch uses the reducer's empty initial value, so the graph returns `[]` rather than `[1, 2, 3]`. The offline repro asserts this specific wrong result and exits non-zero when the fault is present.

This host reproduced the fault with the released issue-era `pydantic-graph==2.0.0b7`; the repository clone was attempted but did not finish under the shared Git workload.

Files:

- `repro.py` — minimal deterministic graph reproduction
- `requirements.txt` — pinned runtime dependency
- `setup_env.sh` — virtual-environment setup
- `run_repro.sh` — single reproduction entrypoint
- `repro_stdout.log` / `repro_stderr.log` — final captured run output
- `reproduction.json` / `reproduction_trajectory.md` — evidence and narrative

Run:

```bash
bash run_repro.sh
```
