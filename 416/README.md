# Bug 416 Repro

This bundle reproduces `pyro-ppl/pyro` issue [#3218](https://github.com/pyro-ppl/pyro/issues/3218).

## What fails

With `torch.set_default_device("cuda")` enabled, `torch.as_tensor(ProvenanceTensor(...))` returns an empty CUDA tensor instead of preserving the original 1D data.

## Files

- `repro.py`: minimal reproduction script
- `requirements.txt`: isolated runtime dependencies
- `setup_env.sh`: creates the venv and installs dependencies
- `run_repro.sh`: runs the repro
- `manifest.json`: benchmark metadata

## Run

```bash
bash run_repro.sh > repro_stdout.log 2> repro_stderr.log
```

The run is expected to fail with an `AssertionError` after printing:

- a working baseline for `torch.as_tensor(y.cuda())`
- the buggy result `tensor([], device='cuda:0')` for `torch.as_tensor(y)` after `torch.set_default_device("cuda")`
