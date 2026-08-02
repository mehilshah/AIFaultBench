# Reproduction Trajectory — Bug 654: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/13764](https://github.com/langflow-ai/langflow/issues/13764)
- **Repository:** langflow-ai/langflow @ `f5ba8f54ca312fef802158fd1fa0d7af964b50e7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the pinned buggy commit.
2. Created `.venv`, installed `dill`, `lfx`, and `redis` at the pinned versions, then installed the backend checkout editable with no unrelated application dependencies.
3. Ran `bash run_repro.sh`. The script replaces `redis.asyncio.StrictRedis` with an `AsyncMock`, so no Redis connection is made, and calls `RedisCache.set` with a dictionary containing a local `ssl.SSLContext`.

## Observed behavior

- `dill.dumps` raised the bare `TypeError: cannot pickle 'SSLContext' object`; `RedisCache.set` leaked it because it catches only `pickle.PicklingError`.
- `run_repro.sh` printed `BUG OBSERVED: RedisCache.set leaked raw TypeError: cannot pickle 'SSLContext' object` and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
