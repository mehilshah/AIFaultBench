# Reproduction Trajectory — Bug 752: llama_index

- **Bug report:** [https://github.com/run-llama/llama_index/issues/20904](https://github.com/run-llama/llama_index/issues/20904)
- **Repository:** run-llama/llama_index @ `7d4436cac2fd0fe488c3330234abcca0310cbeae`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and confirmed the pinned checkout was `7d4436cac2fd0fe488c3330234abcca0310cbeae`.
2. Created a clean virtual environment with the exact pinned dependency set and installed the local `llama-index-core` checkout in editable mode.
3. Ran `repro.py`, which configures `SubQuestionQueryEngine` with an offline France query engine that returns `Paris` and a Germany query engine that raises `RuntimeError("API rate limit exceeded")`.
4. Ran `bash run_repro.sh` for the final captured result.

## Observed behavior

- `run_repro.sh` exited with status 1.
- The reproducer printed `BUG REPRODUCED: RuntimeError escaped failed sub-question`.
- The traceback shows the `RuntimeError: API rate limit exceeded` escaping from `_query_subq` at `sub_question_query_engine.py:263`, rather than the failed sub-question being omitted.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
