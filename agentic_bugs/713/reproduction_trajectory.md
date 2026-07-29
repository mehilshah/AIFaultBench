# Reproduction Trajectory — Bug 713: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/12775](https://github.com/langflow-ai/langflow/issues/12775)
- **Repository:** langflow-ai/langflow @ `737d2c7a61f01ccc5724970abaf687dfeb114bbb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then verified the checkout resolved to `737d2c7a61f01ccc5724970abaf687dfeb114bbb`.
2. Created `.venv` with `bash setup_env.sh`. The repro needs no third-party package because it loads the pinned `validate.py` file and supplies only its import-time dependency names as in-process stubs.
3. Ran `bash run_repro.sh`, which injects an offline fixture module containing `OriginalName` and asks the pinned `create_class()` implementation to execute `from offline_alias_fixture import OriginalName as AliasedName` followed by a reference to `AliasedName`.

## Observed behavior

- The loader stored `OriginalName` rather than `AliasedName` in its generated scope.
- Class creation raised `ValueError`: `Name error (possibly undefined variable): name 'AliasedName' is not defined`.
- `bash run_repro.sh` exited with status 1 after printing the confirmed fault.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
