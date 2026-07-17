# Reproduction Trajectory — Bug 223: triton

- **Bug report:** [https://github.com/triton-inference-server/server/issues/7967](https://github.com/triton-inference-server/server/issues/7967)
- **Repository:** triton-inference-server/server @ `441d7cf`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run ./setup_env.sh to create .venv and install triton==3.7.1.
2. Run ./run_repro.sh or ./.venv/bin/python repro.py from the bug folder.
3. Observe the TypeError raised at len(grid) in triton/runtime/jit.py.

## Observed behavior

- Running the repro in the fresh venv reaches triton/runtime/jit.py line 755 and raises TypeError: object of type 'int' has no len(). The saved logs show the kernel reached the fake compile step before the failure.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
