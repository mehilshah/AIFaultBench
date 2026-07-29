# Reproduction Trajectory — Bug 770: smolagents

- **Bug report:** [https://github.com/huggingface/smolagents/issues/1565](https://github.com/huggingface/smolagents/issues/1565)
- **Repository:** huggingface/smolagents @ `f3c122810a8a2065f24dcd306dfdd46e5d3fcd0d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase/` was at the pinned commit.
2. Created an isolated Python 3.12 environment, installed the exact pinned dependencies, and installed the checkout in editable mode.
3. Ran `bash run_repro.sh`, passing the issue's dict-form message to `LiteLLMModel` with a stub client that raises if inference is reached.

## Observed behavior

- The reproducer printed `OBSERVED BUG: AttributeError: 'dict' object has no attribute 'role'` and exited with status 1.
- The traceback reaches `get_clean_message_list` at `role = message.role`; inference was not attempted because the supplied client stub was never called.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
