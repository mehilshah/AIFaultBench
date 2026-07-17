# Bug 313

This bundle reproduces a GPU stall in `torch_cluster.graclus_cluster` using the
attached edge list from the issue report.

Context:
- Issue: https://github.com/pyg-team/pytorch_geometric/issues/10548
- PyG wrapper: [`codebase/torch_geometric/nn/pool/graclus.py`](codebase/torch_geometric/nn/pool/graclus.py)
- The PyG wrapper is a thin forwarder to `torch_cluster.graclus_cluster`.

Notes:
- The exact reported `torch==2.4.1+cu124` build does not support the current
  GPU in this workspace (`sm_120`), so the repro uses a compatible CUDA stack
  (`torch==2.8.0+cu128`) to exercise the same code path here.
- CPU completes quickly.
- GPU reaches the `graclus_cluster(...)` call and then times out.

Files:
- `batch_edge_index.txt`
- `batch_edge_attr.txt`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```
