# Reproduction Trajectory — Bug 340: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3804](https://github.com/pytorch/rl/issues/3804)
- **Repository:** pytorch/rl @ `62a5fc474f255b0c78b337d9f4abf4428148c5c5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a TensorDictModule(nn.Linear(4, 2)) policy and confirmed its state_dict had 2 keys.
2. Constructed `Evaluator(lambda: GymEnv("CartPole-v1"), policy_bug, max_steps=10)` and evaluated with `TensorDict.from_module(policy_bug).data`.
3. Observed the source module's state_dict drop to 0 keys immediately after evaluate().
4. Verified the deepcopy + cloned TensorDict workaround preserved the original module's 2-key state_dict.

## Observed behavior

- In a clean venv with torch 2.9.1+cpu, tensordict 0.12.4, and gymnasium 1.3.0, the local TorchRL checkout reproduces the issue: `Evaluator.evaluate(TensorDict.from_module(policy_bug).data)` changed `policy_bug.state_dict()` from 2 keys to 0 keys. The workaround case kept the original module at 2 keys.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
