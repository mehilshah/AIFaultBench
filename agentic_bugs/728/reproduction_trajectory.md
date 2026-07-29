# Reproduction Trajectory — Bug 728: semantic-kernel

- **Bug report:** [https://github.com/microsoft/semantic-kernel/issues/13316](https://github.com/microsoft/semantic-kernel/issues/13316)
- **Repository:** microsoft/semantic-kernel @ `1c11258a3242a5a9f8dfa421674fa2108c5e5456`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the required pinned checkout.
2. Created the isolated `.venv` environment, installed .NET SDK 10.0.100 in it, and restored the released issue-era package `Microsoft.SemanticKernel.Connectors.InMemory` 1.66.0-preview into an isolated NuGet cache.
3. Built the report's minimal `net48` project offline with `--no-restore` and checked the build output for the precise assembly versions.

## Observed behavior

- The build emitted `warning MSB3277` for an unresolved `Microsoft.Bcl.AsyncInterfaces` conflict.
- MSBuild reported the conflicting assembly versions as `9.0.0.8` and `9.0.0.9` and chose 9.0.0.8 as primary.
- `repro.py` printed the observed-fault line and exited with status 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
