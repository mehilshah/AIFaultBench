# Reproduction Trajectory — Bug 712: langflow

- **Bug report:** [https://github.com/langflow-ai/langflow/issues/12776](https://github.com/langflow-ai/langflow/issues/12776)
- **Repository:** langflow-ai/langflow @ `737d2c7a61f01ccc5724970abaf687dfeb114bbb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; the full clone was impractically large in the shared environment, so fetched the same pinned SHA shallowly and verified `737d2c7a61f01ccc5724970abaf687dfeb114bbb` in `codebase/`.
2. Created `.venv` with `setup_env.sh`. The reproduction requires no third-party packages: it loads the pinned `lfx.custom.validate` source and stubs only its unrelated import-time dependencies.
3. Passed `prepare_global_scope()` a custom-component module that uses `from __future__ import annotations` and a `TYPE_CHECKING`-only `SomeType` import.

## Observed behavior

- `bash run_repro.sh` exited with status 1 after printing `BUG REPRODUCED: NameError: name 'SomeType' is not defined`.
- The error comes from eagerly evaluating `SomeType` while compiling the class definition without the `__future__` directive. The `TYPE_CHECKING` import is intentionally not executed.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
