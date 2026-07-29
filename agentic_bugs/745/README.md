# Bug 745

Importing `langchain.agents` with Pydantic 2.14.0a1 poisons construction of
`langchain_core.language_models.llms.BaseLLM`: the later import raises
`TypeError: 'function' object is not subscriptable`. The repro imports the
pinned LangChain checkout and does not make any model or provider calls. It
reproduces on this host.

Files: `repro.py` is the assertion-based repro, `requirements.txt` locks its
dependencies, `setup_env.sh` creates the environment, `run_repro.sh` is the
entrypoint, and `repro_stdout.log` / `repro_stderr.log` are the final evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
