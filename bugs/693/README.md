# Bug 693

`SimplePropertyGraphStore.persist` opens its persistence file without specifying UTF-8. On a Windows cp1252 default encoding, graph data containing Chinese characters raises `UnicodeEncodeError`. The repro uses `llama-index-core==0.14.18`, the version reported in the issue, and a local cp1252 filesystem double to deterministically exercise the exact persistence call without an LLM, API key, or network request. It reproduced on this host: the runner exits 1 after observing the expected encoding error.

Files: `repro.py` is the reproducer; `requirements.txt` pins its environment; `setup_env.sh` creates it; `run_repro.sh` runs it; `repro_stdout.log` and `repro_stderr.log` are captured evidence; `reproduction.json` and `reproduction_trajectory.md` record the result.

Run:

```bash
bash run_repro.sh
```
