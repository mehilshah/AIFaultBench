# Reproduction Trajectory — Bug 526: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3309](https://github.com/pytorch/rl/issues/3309)
- **Repository:** pytorch/rl @ `df00d61d31d02465577cbbe8046af449e7685e07`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the local virtual environment and install the pinned runtime dependencies with setup_env.sh
2. Run repro.py via run_repro.sh
3. Observe the UnboundLocalError emitted by CrossQLoss when target_entropy is a numeric value

## Observed behavior

- Running ./run_repro.sh in a clean local venv raises UnboundLocalError: cannot access local variable 'device' where it is not associated with a value. The traceback points to codebase/torchrl/objectives/crossq.py:406 in maybe_init_target_entropy().

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
