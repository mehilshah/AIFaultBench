# Bug 359

Reproduction bundle for [pytorch_geometric issue 10399](https://github.com/pyg-team/pytorch_geometric/issues/10399).

## What fails

`torch.jit.script(HypergraphConv(...))` fails in both modes:

- `use_attention=False`: `Module 'HypergraphConv' has no attribute 'att'`
- `use_attention=True`: `Variable 'alpha' previously had type NoneType but is now being assigned to a value of type Tensor`

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

## Files

- `repro.py`: minimal reproducer
- `requirements.txt`: CPU-only runtime dependencies
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: executes the repro using the local source tree
