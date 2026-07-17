# Reproduction Trajectory — Bug 528: SDV

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/2725](https://github.com/sdv-dev/SDV/issues/2725)
- **Repository:** sdv-dev/SDV @ `ae6e1c01a9b4d06bbc13868071a3ec36c5ed2d33`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created the repro bundle files from the local bug report and codebase.
2. Ran python3.11 repro.py and captured the output in repro_stdout.log and repro_stderr.log.
3. Started ./setup_env.sh to install the runtime dependency set; the install path was Linux-specific and did not reproduce WinError 1114.

## Observed behavior

- The local probe in repro_stdout.log/repro_stderr.log ran on Linux, not Windows, and the workspace did not have numpy, torch, or sdv installed yet. The attempt to bootstrap the environment started resolving Linux wheels and was cancelled before any Windows-style DLL initialization failure could occur.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported error is Windows-specific (WinError 1114 from a DLL initialization routine), but this workspace is Linux, so that exact failure path is not reproducible here.
