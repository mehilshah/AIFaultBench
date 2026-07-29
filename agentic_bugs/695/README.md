# Bug 695

`llama-index-llms-ollama` 0.10.0 accepts an authenticated `async_client`, but
the synchronous `Ollama.complete()` path creates a separate synchronous client
without those headers. The offline repro replaces that newly created client
with a stub and verifies that the request reaches the same unauthenticated
401 path, without making any network or provider calls. This reproduces on
this host.

Files:

- `repro.py` — deterministic offline reproducer
- `requirements.txt` — pinned released integration dependencies
- `setup_env.sh` / `run_repro.sh` — environment setup and entrypoint
- `repro_stdout.log` / `repro_stderr.log` — final captured output
- `reproduction.json` / `reproduction_trajectory.md` — evidence and history

Run with:

```bash
bash run_repro.sh
```
