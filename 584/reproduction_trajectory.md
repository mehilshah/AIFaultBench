# Reproduction Trajectory — Bug 584: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21454](https://github.com/Lightning-AI/pytorch-lightning/issues/21454)
- **Repository:** Lightning-AI/pytorch-lightning @ `027455bcd9433f201b1136f68d54b1a07588abe3`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a custom sampler that records set_epoch calls.
2. Wrap it with DistributedSamplerWrapper(num_replicas=1, rank=0, shuffle=False).
3. Call wrapper.set_epoch(7) and inspect the wrapped sampler.

## Observed behavior

- DistributedSamplerWrapper.set_epoch(7) did not forward to the wrapped sampler: sampler.set_epoch_calls=[], wrapper.epoch=7

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
