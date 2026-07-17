# Reproduction Trajectory — Bug 443: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3515](https://github.com/pytorch/rl/issues/3515)
- **Repository:** pytorch/rl @ `83c2101d3ef92b25e371db24e0b6aca8112ea1dd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a TensorDict with batch_size [1, 2048, 1].
2. Extend a TensorDictReplayBuffer backed by LazyTensorStorage(ndim=3).
3. Observe RuntimeError: batch dimension mismatch, got self.batch_size=torch.Size([1, 2048, 1]) and value.shape=torch.Size([1, 2048, 3]).

## Observed behavior

- replay_buffer.extend(td) raises RuntimeError: batch dimension mismatch for a TensorDict with batch_size [1, 2048, 1]; the failing value shape reported by TorchRL is [1, 2048, 3].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
