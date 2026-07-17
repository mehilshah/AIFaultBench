# Reproduction Trajectory — Bug 122: stable_baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/1928](https://github.com/DLR-RM/stable-baselines3/issues/1928)
- **Repository:** DLR-RM/stable-baselines3 @ `6c00565`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a venv and install the bundle requirements from `requirements.txt`.
2. Instantiate `PPO('MlpPolicy', gym.make('CartPole-v1'), policy_kwargs=dict(net_arch=None))`.
3. Save the model and call `PPO.load()` on the saved artifact.
4. Observe the `TypeError` raised by `len(data['policy_kwargs']['net_arch'])` during load.

## Observed behavior

- Running `bash run_repro.sh` in the prepared venv reproduces `TypeError: object of type 'NoneType' has no len()` from `stable_baselines3/common/base_class.py:695` when `PPO.load()` loads a model saved with `policy_kwargs=dict(net_arch=None)`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
