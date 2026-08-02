# Bug 747

This bundle probes the Pydantic `parsed`-field serializer warning reported for
LangChain OpenAI structured output. It replaces the OpenAI client with a local,
in-memory response and checks the reported public invocation path. On this host,
using the pinned checkout and issue-era dependencies, the warning is not emitted.

Files: `repro.py` contains the offline probe; `requirements.txt` pins the Python
environment; `setup_env.sh` installs the checkout packages; `run_repro.sh` is the
entrypoint; and `repro_stdout.log` / `repro_stderr.log` contain the final evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
