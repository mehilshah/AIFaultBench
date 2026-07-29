# Reproduction Trajectory — Bug 731: camel

- **Bug report:** [https://github.com/camel-ai/camel/issues/4058](https://github.com/camel-ai/camel/issues/4058)
- **Repository:** camel-ai/camel @ `ff7e2d6d32365253e9d4184663fb0f95533d4731`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the recovered issue report and metadata.
2. Ran `bash setup_codebase.sh`. The repository transfer was impractically large on this reference machine and remained incomplete after transferring over 140 MB, so used the public issue-era release `camel-ai==0.2.90` as permitted for a released-package bug.
3. Created the Minimax model through `ModelFactory.create` with `MINIMAX_API_BASE_URL` absent, a non-secret placeholder API key, and inert synchronous/asynchronous clients. This executes only constructor configuration; it cannot send a provider request.
4. Asserted that the selected URL is the international endpoint, then ran `bash run_repro.sh`.

## Observed behavior

- The script printed `OBSERVED_MINIMAX_DEFAULT_URL=https://api.minimaxi.com/v1`.
- It exited with status 1 and raised `AssertionError`, because the expected international endpoint is `https://api.minimax.io/v1`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
