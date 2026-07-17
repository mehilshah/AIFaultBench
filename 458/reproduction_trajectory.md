# Reproduction Trajectory — Bug 458: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3508](https://github.com/pytorch/rl/issues/3508)
- **Repository:** pytorch/rl @ `05212b82d764d1c4ca06e36b3220ce9c401882da`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created an isolated venv and installed the reported dependency set.
2. Ran the minimal constructor from the local torchrl checkout with PYTHONPATH pointing at codebase/.
3. Observed the exact RuntimeError from torchrl/data/replay_buffers/samplers.py:_init.

## Observed behavior

- In a clean Python 3.12 virtualenv with torch 2.8.0, tensordict 0.11.0, and the checked-out torchrl commit, running the reported constructor prints a warning that the torchrl C++ extension is not available and then raises RuntimeError: SumSegmentTreeFp32 is not available. See warning above.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
