# Reproduction Trajectory — Bug 684: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/14227](https://github.com/langflow-ai/langflow/issues/14227)
- **Repository:** langflow-ai/langflow @ `0a8ef930283447d6411b71ebf3df3c627ea5e8a8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to fetch the pinned Langflow source and inspected its lockfile, which pins the reported import-time dependency to `mem0ai==2.0.12`.
2. Created `.venv` and installed the pinned `mem0ai` dependency graph in `requirements.txt`. The focused dependency reproduction is permitted because Langflow's full optional provider bundle is much larger and the reported stack reaches this dependency before Langflow starts serving.
3. Ran `bash run_repro.sh`. The script sets `HOME=/snap/bare/5`, a real read-only mount on this host, removes `MEM0_DIR`, and imports `mem0`. It does not construct a model client or make a network call.

## Observed behavior

- `mem0ai==2.0.12` calls `os.makedirs(~/.mem0, exist_ok=True)` during import and propagates `OSError: [Errno 30] Read-only file system: '/snap/bare/5/.mem0'`.
- The repro verified that exact exception and exited with status 1, demonstrating the startup-blocking fault in the issue.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
