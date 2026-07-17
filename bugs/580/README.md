# Bug 580 Reproduction Bundle

This folder reproduces the `train_without_ext_pred=True` failure reported for
`examples/llm/glem.py` in PyTorch Geometric issue 9899.

## What fails

`torch_geometric.nn.models.GLEM.train()` unconditionally executes
`pseudo_labels.to(self.device)`. In the `train_without_ext_pred` path,
`examples/llm/glem.py` passes `ext_pseudo_labels=None` into that call during
the GNN pretraining stage, so the method crashes with:

`AttributeError: 'NoneType' object has no attribute 'to'`

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is intentionally minimal. It loads the real
`codebase/torch_geometric/nn/models/glem.py` module from this folder and stubs
only the unavailable runtime pieces needed to reach the failing call.

