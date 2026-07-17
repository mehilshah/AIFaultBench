# Reproduction Trajectory — Bug 121: stable_baselines3

- **Bug report:** [https://github.com/DLR-RM/stable-baselines3/issues/1900](https://github.com/DLR-RM/stable-baselines3/issues/1900)
- **Repository:** DLR-RM/stable-baselines3 @ `5623d98`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a PPO model on IdentityEnvBox with learning_rate=lambda _: np.sin(1.0).
2. Save the model to a zip archive.
3. Call PPO.load() on the saved archive.

## Observed behavior

- UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options 
	(1) Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
	(2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
	WeightsUnpickler error: Unsupported global: GLOBAL numpy.core.multiarray.scalar was not an allowed global by default. Please use `torch.serialization.add_safe_globals([scalar])` to allowlist this global if you trust this class/function.

Check the documentation of torch.load to learn more about types accepted by default with weights_only https://pytorch.org/docs/stable/generated/torch.load.html.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
