# Reproduction Trajectory — Bug 734: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/5911](https://github.com/mem0ai/mem0/issues/5911)
- **Repository:** mem0ai/mem0 @ `f38608fb5061c5aa067793740447cf217b3afee0`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; its initial clone was interrupted by concurrent clone traffic, so fetched and checked out the same pinned commit directly, then verified `git rev-parse HEAD`.
2. Created `.venv`, installed the pinned runtime dependencies and the checked-out package in editable mode.
3. Called `Memory.add()` with procedural-memory input, an `agent_id`, and a plain placeholder object supplied as `llm`. Python rejects the undeclared keyword before the method body, so no provider, model, or storage call is possible.
4. Ran `bash run_repro.sh` and captured its stdout and stderr.

## Observed behavior

- `Memory.add()` raised `TypeError: Memory.add() got an unexpected keyword argument 'llm'` and the reproducer exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
