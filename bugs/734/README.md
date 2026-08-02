# Bug 734

At commit `f38608f`, synchronous `Memory.add()` does not declare the `llm`
keyword that its asynchronous counterpart accepts. The offline reproduction
calls that public method with a placeholder custom model and verifies that
Python raises the reported `TypeError` before any model, storage, or network
operation can occur. The bug reproduces on this host (the script intentionally
exits with status 1 when it observes the buggy behavior).

Files: `repro.py` is the minimal check; `requirements.txt` pins its runtime
dependencies; `setup_env.sh` builds the venv; `run_repro.sh` is the entrypoint;
and `repro_stdout.log` / `repro_stderr.log` are the final-run evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
