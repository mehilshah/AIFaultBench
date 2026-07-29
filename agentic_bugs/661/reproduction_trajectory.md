# Reproduction Trajectory — Bug 661: crewAI

- **Bug report:** [https://github.com/crewAIInc/crewAI/issues/5607](https://github.com/crewAIInc/crewAI/issues/5607)
- **Repository:** crewAIInc/crewAI @ `b0e2fda105c2e0c05c7abb1f53800443ffd582ea`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified that `codebase/` was detached at the pinned commit.
2. Created `.venv` with `a2a-sdk==1.0.1`, `pydantic==2.11.10`, `httpx==0.28.1`, and `PyJWT==2.10.1`; installed the pinned CrewAI package editable without resolving unrelated CrewAI features.
3. Ran `bash run_repro.sh`. The script loads the pinned A2A configuration path, constructs `A2AClientConfig` with a localhost endpoint, and makes no network request.

## Observed behavior

- `run_repro.sh` exited with status 1.
- stdout printed `OBSERVED BUG with a2a-sdk 1.0.1: cannot import name 'A2AClientHTTPError' from 'a2a.client.errors'`.
- The traceback shows `A2AClientConfig` calling `_get_default_update_config`, then CrewAI's polling handler importing the removed symbol from `a2a.client.errors`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
