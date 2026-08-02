# Bug 654

On the pinned Langflow checkout, `RedisCache.set` only catches `pickle.PicklingError` even though `dill` raises a bare `TypeError` for a live `ssl.SSLContext`. This reproduction uses a mocked Redis client and a local SSL context to confirm that the raw error leaks from the cache write; on this host the bug is reproduced.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` pins its dependencies; `setup_env.sh` creates the environment; `run_repro.sh` is the entrypoint; and `repro_stdout.log`/`repro_stderr.log` are captured evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
