# Reproduction Trajectory — Bug 741: phoenix

- **Bug report:** [https://github.com/Arize-ai/phoenix/issues/13775](https://github.com/Arize-ai/phoenix/issues/13775)
- **Repository:** Arize-ai/phoenix @ `031975ccbe60e50967d8f192b6dfe6ca6de1daa7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. The full monorepo clone was still unpacking Git objects, and the fault is also present in the released issue-era `arize-phoenix-otel==0.16.0` package, so I used that permitted released-package fallback.
2. Created `.venv` and installed the exact package pin with no optional telemetry dependencies.
3. Loaded only `phoenix/otel/settings.py` from that installed wheel and called `parse_env_headers("x=a,bad")`.

## Observed behavior

- The call printed `OBSERVED BUG: parse_env_headers('x=a,bad') raised ValueError: not enough values to unpack (expected 2, got 1)` and exited non-zero.
- The traceback locates the failing unpack at `phoenix/otel/settings.py`, line 135: `name, value = parts`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
