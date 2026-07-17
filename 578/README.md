# Pyro param device repro

This bundle targets the reported issue:

`pyro.param("alpha_loc", torch.rand(3).cuda()).device`

The standardized machine can install the branch with Torch 1.13.1+cpu, but it
does not expose a CUDA device. As a result, the CUDA-only snippet cannot be
executed here.

## Files

- `repro.py`: checks the environment and runs the exact parameter path only when CUDA is available.
- `setup_env.sh`: builds a local Python 3.10 virtual environment and installs the pinned dependencies.
- `run_repro.sh`: runs setup plus the repro and writes `repro_stdout.log` / `repro_stderr.log`.
- `reproduction.json`: machine-readable result for this folder.

## Result on this machine

The reproduction is not observable here because `torch.cuda.is_available()`
is `False`.

## Reproduction command

```bash
bash run_repro.sh
```
