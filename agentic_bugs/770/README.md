# Bug 770

At the pinned smolagents commit, the documented dict-form chat message crashes `LiteLLMModel` before inference: message normalization expects a `ChatMessage` dataclass and accesses `message.role`. The local reproducer supplies that input with a stub client, checks the exact `AttributeError`, and exits non-zero, so it makes no API or provider request. The fault reproduced on this host.

Files: `repro.py` is the deterministic reproducer; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run the isolated environment; `repro_stdout.log` and `repro_stderr.log` are final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
