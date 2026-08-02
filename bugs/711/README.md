# Bug 711

CAMEL's async streaming tool-error path records a `tool` response after a tool raises but drops the preceding assistant `tool_calls` message, leaving an invalid OpenAI conversation sequence. The offline reproducer uses CAMEL's local `StubModel` and a deterministic failing async tool, then asserts that the resulting memory contains the orphaned tool response. On this host the bug reproduces: `run_repro.sh` exits 1 with the targeted assertion.

Files: `repro.py` (reproducer), `requirements.txt` (pinned compatibility dependency), `setup_env.sh` (environment setup), `run_repro.sh` (entrypoint), `repro_stdout.log` and `repro_stderr.log` (final-run evidence), `reproduction.json` (machine-readable verdict), and `reproduction_trajectory.md` (run narrative).

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
