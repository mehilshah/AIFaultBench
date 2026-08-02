# Reproduction Trajectory — Bug 698: smolagents

- **Bug report:** [https://github.com/huggingface/smolagents/issues/1799](https://github.com/huggingface/smolagents/issues/1799)
- **Repository:** huggingface/smolagents @ `f76dee172666d7dad178aed06b257c629967733b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, which cloned the repository and checked out `f76dee172666d7dad178aed06b257c629967733b`.
2. Created `.venv`, installed the exact direct runtime dependencies, and installed the pinned checkout editable.
3. Ran an offline script that subclasses `CodeAgent`, overrides `create_python_executor()`, and instantiates it with `executor_type="my_executor"` and an object model double.

## Observed behavior

- The constructor raised `ValueError: Unsupported executor type: my_executor`.
- The subclass's overridden executor factory was not called, demonstrating that validation occurred before the overridable factory.
- `bash run_repro.sh` exited with status 1, as required to signal the buggy behavior.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
