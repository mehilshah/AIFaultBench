# Reproduction Trajectory — Bug 603: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2008](https://github.com/pyro-ppl/numpyro/issues/2008)
- **Repository:** pyro-ppl/numpyro @ `0e1bdbacd6bbb502cf40d12948a822913e625794`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a virtualenv and install the pinned runtime from requirements.txt plus the local codebase in editable mode.
2. Run ./run_repro.sh --iters 10 to execute the synthetic classroom SVI loop.
3. Observe that the same repeated SVI.update path completes while RSS rises by about 770 MB over 10 iterations.

## Observed behavior

- The synthetic repro based on the reported model structure ran successfully on this host and showed steady resident-memory growth across repeated SVI updates: initial RSS 454.27 MB, then 816.87 MB at iter 0, 998.19 MB at iter 4, and 1224.75 MB at iter 9. The run completed without exception, but the macOS-specific Mach-port counter is not observable on Linux.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./setup_env.sh && ./run_repro.sh --iters 10
```
