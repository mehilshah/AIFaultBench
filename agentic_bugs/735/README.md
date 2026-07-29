# Bug 735

The FAISS vector store returns a bare empty list when its index is uninitialized,
although callers require a nested list. The repro creates that state and asserts
that the observed `[]` violates the expected `[[]]` contract. On this host, the
fault is reproduced without any model, API key, or network call at runtime.

Files: `repro.py` is the minimal check; `requirements.txt` and `setup_env.sh`
create its environment; `run_repro.sh` runs it; the log and JSON files record
the final evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
