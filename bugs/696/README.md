# Bug 696

`ContextChatEngine._aget_nodes()` takes an async retrieval path but dispatches node postprocessing through the synchronous hook. The reproduction uses a local dummy retriever, fake LLM metadata, and tracking postprocessor to prove that `postprocess_nodes()` is called while `apostprocess_nodes()` is skipped; it reproduces on this host with `llama-index-core==0.14.15` and makes no model or service calls.

The full repository clone was impractically slow here, so the issue-reported released package is pinned in `requirements.txt` instead. The final run exits 1 deliberately once the faulty dispatch is observed.

Files:

- `repro.py` — deterministic reproduction.
- `requirements.txt` — pinned released dependency.
- `setup_env.sh` and `run_repro.sh` — environment setup and single run entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — output from the final run.
- `reproduction.json` and `reproduction_trajectory.md` — structured and narrative evidence.

Run:

```bash
bash run_repro.sh
```
