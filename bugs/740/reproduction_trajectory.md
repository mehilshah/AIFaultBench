# Reproduction Trajectory — Bug 740: phoenix

- **Bug report:** [https://github.com/Arize-ai/phoenix/issues/13777](https://github.com/Arize-ai/phoenix/issues/13777)
- **Repository:** Arize-ai/phoenix @ `031975ccbe60e50967d8f192b6dfe6ca6de1daa7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`. Its full clone remained incomplete in this process host, so fetched the exact pinned commit at depth 1 into `codebase/` and checked it out as `031975ccbe60e50967d8f192b6dfe6ca6de1daa7`.
2. Created `.venv`, installed the exact pinned dependencies, and installed `packages/phoenix-client` from that checkout in editable mode with `bash setup_env.sh`.
3. Ran `bash run_repro.sh`, which validates a minimal valid ATIF-v1.4 trajectory containing the malformed present timestamp `not-a-date`, then converts it.

## Observed behavior

- Validation returned successfully for the malformed timestamp.
- Conversion raised the exact parser error `ValueError: Invalid isoformat string: 'not-a-date'`; the reproduction printed its bug marker and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
