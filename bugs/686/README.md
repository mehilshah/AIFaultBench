# Bug 686

`ChatAnthropic.bind_tools()` misclassifies Anthropic's `advisor_20260301`
server-side tool as a normal function tool and raises `KeyError: 'parameters'`.
The offline repro binds that tool with a dummy API key and asserts the precise
failure before any model invocation or network request. The bug reproduces on
this host.

Files: `repro.py` is the reproducer; `requirements.txt` and `setup_env.sh`
build its environment; `run_repro.sh` is the entrypoint; and the log, JSON, and
trajectory files record the observed result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
