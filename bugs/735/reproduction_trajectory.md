# Reproduction Trajectory — Bug 735: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/5724](https://github.com/mem0ai/mem0/issues/5724)
- **Repository:** mem0ai/mem0 @ `e615cc66de7ae8e356d7c37b98200016a32e1d0f`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; its initial full Git transfer did not complete on this host, so retrieved the same pinned commit with a filtered Git fetch and verified its SHA.
2. Created `.venv`, installed the exact pinned dependencies, and installed that checkout in editable mode.
3. Constructed a local `FAISS` store, set `store.index = None`, and invoked `list(filters={"user_id": "alice"})` using `bash run_repro.sh`.

## Observed behavior

- `FAISS.list()` returned the bare list `[]`, where its initialized path returns a nested result and callers require `[[]]`.
- The repro printed `OBSERVED BUG: FAISS.list() returned []; expected [[]]` and exited non-zero with `AssertionError: uninitialized FAISS.list() violates its List[List[OutputData]] contract`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
