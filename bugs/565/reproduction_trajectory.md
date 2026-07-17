# Reproduction Trajectory — Bug 565: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3014](https://github.com/pyro-ppl/pyro/issues/3014)
- **Repository:** pyro-ppl/pyro @ `319c515de2a82ac002516ccd4b44dda8e32f7ac4`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Set up the pinned CUDA PyTorch environment and install the local editable Pyro codebase.
2. Run `bash run_repro.sh` to execute the model-side enumeration repro on GPU.
3. Observe monotonic GPU memory growth in repro_stdout.log.

## Observed behavior

- On CUDA capability (12, 0), the model-side TraceEnum_ELBO repro grew torch.cuda.memory_allocated() from 1536 bytes to 103424 bytes over 200 SVI steps (ups=199).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
