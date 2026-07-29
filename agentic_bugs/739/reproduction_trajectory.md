# Reproduction Trajectory — Bug 739: phoenix

- **Bug report:** [https://github.com/Arize-ai/phoenix/issues/13780](https://github.com/Arize-ai/phoenix/issues/13780)
- **Repository:** Arize-ai/phoenix @ `031975ccbe60e50967d8f192b6dfe6ca6de1daa7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; when its full-history clone did not finish, fetched the exact pinned commit shallowly into the same clone and checked it out.
2. Created an isolated Python 3.12 environment and installed the pinned phoenix-client dependencies and editable package.
3. Constructed a deterministic two-step ATIF-v1.4 trajectory whose agent step has `metrics: "oops"`.
4. Ran the repository validator and then converter through `bash run_repro.sh`.

## Observed behavior

- Validation printed `VALIDATION_ACCEPTED_NON_OBJECT_METRICS`, proving it accepted the non-object metrics value.
- Conversion raised `AttributeError: 'str' object has no attribute 'get'`; `run_repro.sh` exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
