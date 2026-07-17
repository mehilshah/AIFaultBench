# Reproduction Trajectory — Bug 429: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3549](https://github.com/pytorch/rl/issues/3549)
- **Repository:** pytorch/rl @ `1ed0d1e40f590420a123006affb958b4c02b0b8c`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Checked out the referenced upstream snapshot with `setup_codebase.sh`.
2. Added a minimal repro harness that imports the local `torchrl` source and attempts the exact `GymEnv("HalfCheetah-v4")` + `SyncDataCollector(..., device="mps", env_device="mps")` path from the report.
3. Ran `./run_repro.sh`; it exited with a Linux/MPS blocking message before the collector could be constructed.

## Observed behavior

- The bundle's repro harness exits immediately on this host with `BLOCKED: the reported crash requires macOS with Apple MPS; current host is Linux.` The original issue is explicitly MPS-specific, so the collector path cannot be exercised here.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

This environment is Linux and does not provide Apple MPS, but the reported crash requires macOS with an available MPS backend.
