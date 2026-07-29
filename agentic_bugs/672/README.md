# Bug 672

At the pinned Agno revision, `Workflow.get_session()` calls an asynchronous
database backend's `get_session()` method without awaiting it. The offline
reproduction provides a fake `AsyncBaseDb` containing a real
`WorkflowSession`, verifies the async helper can load it, and then verifies the
sync helper returns `None` and produces the unawaited-coroutine warning.

The fault reproduces on this host: `run_repro.sh` exits with status 1 after
printing the observed broken session load.

Files:

- `repro.py` — minimal offline reproduction.
- `requirements.txt` — pinned Python dependencies.
- `setup_env.sh` — creates the environment and installs the editable checkout.
- `run_repro.sh` — one-command reproduction entrypoint.
- `repro_stdout.log` and `repro_stderr.log` — captured final-run evidence.
- `reproduction.json` and `reproduction_trajectory.md` — result metadata.

Run it with:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
