# Bug 718

browser-use 0.12.6 rejects a valid structured response when an OpenAI-compatible reasoning model returns its JSON in `reasoning_content` and leaves `content` empty. The offline repro supplies that recorded response to the pinned `ChatOpenAI` adapter and checks that it fails with the report's EOF invalid-JSON error. It reproduces on this host.

Files: `repro.py` is the deterministic reproduction; `requirements.txt`, `setup_env.sh`, and `run_repro.sh` create and run its environment; `repro_stdout.log` and `repro_stderr.log` contain final-run evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
