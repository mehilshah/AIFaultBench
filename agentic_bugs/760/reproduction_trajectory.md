# Reproduction Trajectory — Bug 760: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6008](https://github.com/pydantic/pydantic-ai/issues/6008)
- **Repository:** pydantic/pydantic-ai @ `88fb4e34eb24bb39d08a900bfe5f631d7df49484`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the issue's supplied graph-only reproduction and maintainer comment describing the duplicate reducer.
2. Ran `bash setup_codebase.sh`; the shared host did not complete the clone amid concurrent Git operations, so used the released issue-era `pydantic-graph==2.0.0b7` package, as permitted for released-package bugs.
3. Created `.venv`, installed the pinned package, and ran `bash run_repro.sh` with no model client, API key, or network activity at runtime.

## Observed behavior

- `run_repro.sh` exited with status 1 and printed `FAULT: pydantic-graph=2.0.0b7; downstream_join_id returned []; join emitted [[], [1, 2, 3]]`.
- The non-empty map therefore dispatches the post-join node first with the reducer's initial `[]`, then with `[1, 2, 3]`; the graph returns the erroneous first value.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
