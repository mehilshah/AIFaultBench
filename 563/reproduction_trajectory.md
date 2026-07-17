# Reproduction Trajectory — Bug 563: rl

- **Bug report:** [https://github.com/pytorch/rl/issues/3260](https://github.com/pytorch/rl/issues/3260)
- **Repository:** pytorch/rl @ `9354783e3dc41f69b252992c8dd6526a3ad981f2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean venv and install torch 2.7.1 + tensordict 0.10.0.
2. Run repro.py with the local codebase on PYTHONPATH.
3. Observe check_env_specs fail with a next-key mismatch between real and fake TensorDicts.

## Observed behavior

- Running the minimal nested multi-agent env against the local torchrl source raises AssertionError in check_env_specs: real contains ('next', 'agents', 'actions'), ('next', 'randomStates'), and ('next', 'reward') that fake_tensordict does not generate.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
