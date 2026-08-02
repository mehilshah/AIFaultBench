# Bug 657

`ChatAnthropic` forwards a `SystemMessage` text content block verbatim, leaking
the LangChain-generated `id` into Anthropic's `system` payload. The offline repro
calls `ChatAnthropic.invoke` with a local schema-validating client and confirms
that it receives the unsupported field; no API key or network request is used.
The fault reproduces on this host (the script intentionally exits 1).

Files: `repro.py` is the reproducer; `requirements.txt` pins runtime dependencies;
`setup_env.sh` creates the environment; `run_repro.sh` runs it; the two log files
contain the final captured output; and `reproduction.json` records the verdict.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
