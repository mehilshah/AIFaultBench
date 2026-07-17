# Reproduction Trajectory — Bug 252: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3056](https://github.com/pytorch/rl/issues/3056)
- **Repository:** pytorch/rl @ `7e8f940`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean Python 3.12 virtual environment and installed torch==2.7.1+cpu, tensordict==0.9.0, numpy==2.3.1, orjson==3.10.18, cloudpickle==3.1.2, and packaging==26.2.
2. Ran repro.py with PYTHONPATH pointing at the local codebase and a pure-Python segment-tree shim so PrioritizedSampler could save and load state without the missing C++ binary.
3. Observed the crash in PrioritizedSampler.loads() before metadata application completed.

## Observed behavior

- run_repro.sh exited with status 1 and repro_stderr.log ends with AttributeError: 'NoneType' object has no attribute 'copy_' in torchrl/data/replay_buffers/samplers.py:742.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
