# Reproduction Trajectory — Bug 727: openai-agents-python

- **Bug report:** [https://github.com/openai/openai-agents-python/issues/2962](https://github.com/openai/openai-agents-python/issues/2962)
- **Repository:** openai/openai-agents-python @ `da82b2cd663ee263b206ce65179c26b598d61f73`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and checked out the supplied pinned commit. The reference terminal interrupted the foreground full clone, so the same repository was fetched directly at the pinned commit to complete the checkout.
2. Created `.venv`, installed the exact dependency versions in `requirements.txt`, and installed the pinned checkout in editable mode.
3. Ran the pinned `BaseSandboxSession._validate_remote_path_access` method with Windows `pathlib` semantics and an in-memory recording sandbox. No Modal, provider, or LLM calls are made.

## Observed behavior

- The command passed to the Linux sandbox was `\tmp\openai-agents\bin\resolve-workspace-path-f8e24896b498 \workspace \workspace 1`, rather than a command beginning with the required POSIX executable path `/tmp/openai-agents/bin/resolve-workspace-path-f8e24896b498`.
- The repro raised `AssertionError: BUG REPRODUCED: Windows backslashes make the Linux helper unfindable` and exited non-zero.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
