# Reproduction Trajectory — Bug 491: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3409](https://github.com/pytorch/rl/issues/3409)
- **Repository:** pytorch/rl @ `05aa8a8029e989a6091ff1b14a60892d194397fb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Composite spec with shape=(2,) and a bounded 'obs' leaf.
2. Sample from the spec and convert the sampled tensor to a plain dict of numpy arrays.
3. Call Composite.encode() on the dict input.
4. Observe that the returned TensorDict has batch_size=torch.Size([]) instead of torch.Size([2]).

## Observed behavior

- Running the repro in a clean virtualenv produced: torch.Size([2]), torch.Size([2]), torch.Size([]), and matches_expected: False. That confirms Composite.encode() returns a TensorDict with an empty batch_size for a dict input.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
