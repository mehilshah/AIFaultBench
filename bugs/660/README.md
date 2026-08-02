# Bug 660

The report claimed that `Send` objects cannot be checkpointed because the
msgpack serializer raises `TypeError`. At the pinned source, LangGraph's
`JsonPlusSerializer` round-trips `Send` and a checkpointed graph using the
supported conditional-edge `Send` pattern completes successfully. The report's
node-return example instead fails with `InvalidUpdateError`, before any alleged
serialization failure. The result on this host is not reproduced.

Files:

- `repro.py` — deterministic offline verification of the raw msgpack,
  serializer, reported graph, and supported graph paths.
- `requirements.txt` — exact third-party dependency pins.
- `setup_env.sh` and `run_repro.sh` — environment bootstrap and one-command
  runner.
- `repro_stdout.log` and `repro_stderr.log` — captured output from the final
  run.
- `reproduction.json` and `reproduction_trajectory.md` — evidence and
  narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
