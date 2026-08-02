# Reproduction Trajectory — Bug 773: browser-use

- **Bug report:** [https://github.com/browser-use/browser-use/issues/4267](https://github.com/browser-use/browser-use/issues/4267)
- **Repository:** browser-use/browser-use @ `bf7775dc85e117612e66d8504c28384abecf3b6c`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to clone the repository at the pinned commit.
2. Created `.venv` and installed the editable pinned checkout with `bash setup_env.sh`.
3. Constructed the real `Agent` class using an offline model double; the double raises if invoked, so no provider call can occur.
4. Called `session_to_python_script(agent)` and captured the final `bash run_repro.sh` output.

## Observed behavior

- `session_to_python_script` immediately evaluated `agent.session.cells` and raised `AttributeError: 'Agent' object has no attribute 'session'`.
- The reproduction exited with status 1, as required to signal that the buggy behavior is present.
- Standard error was empty; no browser, LLM, or third-party runtime request was made.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
