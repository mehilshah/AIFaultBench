# Bug 742

AutoGen 0.7.2 calls `ChatCompletionToolParam(...)` while converting a valid tool schema. With the reported `openai==1.99.3`, that symbol is a `typing.Union`, so conversion fails before any model or network call. The current result on this host is reproduced.

Files: `repro.py` is the offline trigger; `requirements.txt` pins the reported SDK; `setup_env.sh` builds the environment; `run_repro.sh` runs it; and the log, JSON, and trajectory files hold the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
