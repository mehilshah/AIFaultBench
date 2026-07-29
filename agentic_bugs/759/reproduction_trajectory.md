# Reproduction Trajectory — Bug 759: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6025](https://github.com/pydantic/pydantic-ai/issues/6025)
- **Repository:** pydantic/pydantic-ai @ `e19e18065a13be0490483ad3c5601d232af8185b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase/` was checked out at the pinned buggy commit.
2. Ran `bash run_repro.sh`; it bootstrapped `.venv`, installed the local slim and graph workspace packages, and executed the offline reproduction.
3. The script drove two Vercel AI adapter turns with `TestModel`, a server-managed system prompt, and no provider or network access.

## Observed behavior

- Turn 1 returned `['ModelRequest', 'ModelResponse']` from `new_messages()`, leaking the inbound user request.
- Turn 2 returned `['ModelResponse']`, so the regression is asymmetric as reported.
- The final assertion raised `AssertionError: BUG: turn 1 new_messages() includes the inbound user ModelRequest` and the command exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
