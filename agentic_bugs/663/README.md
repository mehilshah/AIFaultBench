# Bug 663

`RedisKVStore.get_all` assumes each Redis hash key is `bytes` and unconditionally calls `.decode()`. With `decode_responses=True`, Redis supplies a `str`, so the method raises `AttributeError`. The offline repro double supplies that `str` key and verifies the precise exception from the pinned buggy checkout; on this host the bug reproduces.

Files: `repro.py` contains the deterministic reproduction; `requirements.txt` pins its direct dependencies; `setup_env.sh` creates the environment; `run_repro.sh` is the entrypoint; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
