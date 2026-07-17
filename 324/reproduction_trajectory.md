# Reproduction Trajectory — Bug 324: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3840](https://github.com/pytorch/rl/issues/3840)
- **Repository:** pytorch/rl @ `a1a107003252a3ab2a0830702d21b7f46caff6d7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtualenv and installed the runtime dependencies listed in requirements.txt.
2. Ran the local repro script against the checked-out codebase with 16 workers and a 1.1 second SleepEnv step delay.
3. Observed the expected timing gap: about 17 seconds at preemptive_threshold=1.0 versus about 2 seconds at 0.99.

## Observed behavior

- Running ./run_repro.sh in an isolated Python 3.12 venv with torch 2.7.1+cpu, tensordict 0.13.0, and gymnasium 1.1.1 produced: preemptive_threshold=1.0, elapsed=17.070s; preemptive_threshold=0.99, elapsed=1.973s; bug_reproduced=yes.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
