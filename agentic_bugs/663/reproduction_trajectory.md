# Reproduction Trajectory — Bug 663: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/22115](https://github.com/run-llama/llama_index/issues/22115)
- **Repository:** run-llama/llama_index @ `9f66e8a649856524ef0ff081a23d58cd071b6ae4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out the requested pinned revision.
2. Created `.venv`, installed the two pinned runtime dependencies, and installed the Redis KV-store integration editable from that checkout.
3. Ran `bash run_repro.sh`. The script supplies an offline Redis double that yields a `str` hash key, as `redis` does with `decode_responses=True`.

## Observed behavior

- `run_repro.sh` exited with status 1 after `RedisKVStore.get_all` raised `AttributeError: 'str' object has no attribute 'decode'`.
- The traceback points to `base.py` line 161, where the buggy checkout unconditionally evaluates `key.decode()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
