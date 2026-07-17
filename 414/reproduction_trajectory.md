# Reproduction Trajectory — Bug 414: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3550](https://github.com/pytorch/rl/issues/3550)
- **Repository:** pytorch/rl @ `b6326f7726429241a66c888c4d70d588049f77a9`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Clone the pinned pytorch/rl checkout into ./codebase.
2. Inspect the repo and confirm the MPS float64 downcast fix is already present in this snapshot.
3. Run the repro entrypoint on this Linux host.

## Observed behavior

- The pinned checkout is b6326f7726429241a66c888c4d70d588049f77a9, whose commit message is '[Bugfix] Add MPS float64->float32 downcast (#3548)'.
- The local host is Linux, not macOS, so Apple MPS cannot be exercised here.
- The repro script is guarded to short-circuit with a blocking reason on non-Darwin systems.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This environment is Linux, while the issue is specific to macOS MPS; the exact failing device backend is unavailable here.
