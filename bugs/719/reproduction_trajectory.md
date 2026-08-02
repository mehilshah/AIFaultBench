# Reproduction Trajectory — Bug 719: browser-use

- **Bug report:** [https://github.com/browser-use/browser-use/issues/4676](https://github.com/browser-use/browser-use/issues/4676)
- **Repository:** browser-use/browser-use @ `ef32ed708ad90b3cffea0b622d54002c0c5fd94a`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the full Git checkout did not complete on this reference machine.
2. Used the released issue-era package `browser-use==0.12.6` instead, with `langchain-openai==1.1.7` and `langchain-core==1.5.2` installed in `.venv`.
3. Created the report's `CustomDeepSeek(ChatOpenAI)` subclass and registered it with `browser_use.tokens.service.TokenCost`.
4. Called the tracked model with a Pydantic output model. The invalid `127.0.0.1:9` base URL ensures any unexpected request remains local; the failure occurred before a request.
5. Ran `bash run_repro.sh` and captured the final non-zero run.

## Observed behavior

- `run_repro.sh` exited with status 1 and printed `OBSERVED BUG: AttributeError: items`.
- `TokenCost.tracked_ainvoke` passed Browser Use's Pydantic output model as the second positional argument to LangChain's `ainvoke`; LangChain treated it as `config` and raised `AttributeError: items` at `config.items()`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
